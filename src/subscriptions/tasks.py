from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.db import transaction
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from subscriptions.models import NOTIFICATION_DAYS_THRESHOLD, UserSubscription


@shared_task
def process_expired_subscriptions():
    try:
        with transaction.atomic():
            expired_count = UserSubscription.objects.filter(
                is_active=True, expiration_date__lte=timezone.now()
            ).update(
                is_active=False,
                paypal_subscription_id=None,
                expiration_notification_sent=False,
            )

            if expired_count == 0:
                return _("No expired subscriptions found.")

    except Exception as e:
        return _(f"An error occurred while processing expired subscriptions: {str(e)}")


@shared_task
def send_subscription_expiring_email(user_subscription_id: int):
    try:
        user_subscription = UserSubscription.objects.select_related("user", "plan").get(
            id=user_subscription_id
        )

        if user_subscription.expiration_notification_sent:
            return _(
                f"Expiration notification already sent for {user_subscription.user.email}"
            )

        user = user_subscription.user
        days_left = user_subscription.days_until_expiry

        if days_left is None or days_left > NOTIFICATION_DAYS_THRESHOLD:
            return _(f"No expiration notification needed for {user.email}")

        mail_subject = _("Your subscription is expiring soon")
        domain = settings.SITE_DOMAIN

        message = render_to_string(
            template_name="emails/subscription_expiring_email.html",
            context={
                "user": user,
                "subscription": user_subscription,
                "domain": domain,
                "days_left": days_left,
            },
        )

        email = EmailMessage(
            subject=mail_subject,
            body=message,
            to=[user.email],
            from_email=settings.EMAIL_HOST_USER,
        )
        email.content_subtype = "html"
        email.send()

        user_subscription.expiration_notification_sent = True
        user_subscription.save(update_fields=["expiration_notification_sent"])

        return _(f"Expiration notification sent to {user.email}")

    except UserSubscription.DoesNotExist:
        return _("User subscription not found.")

    except Exception as e:
        return _(
            f"An error occurred while sending the expiration notification: {str(e)}"
        )


@shared_task
def check_subscriptions_for_notification():
    try:
        subscriptions_to_notify = UserSubscription.objects.filter(
            is_active=True,
            expiration_date__isnull=False,
            expiration_notification_sent=False,
        )

        sent_count = 0
        for subscription in subscriptions_to_notify:
            if subscription.send_expiration_notification:
                send_subscription_expiring_email.delay(subscription.id)
                sent_count += 1

        return f"Scheduled {sent_count} expiration notifications using model method"

    except Exception as e:
        return f"Error checking subscriptions for notification: {str(e)}"
