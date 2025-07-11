from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from core.utils.token_generator import TokenGenerator


@shared_task
def send_registration_email(user_id: int) -> None:
    try:
        User = get_user_model()
        user_instance = User.objects.get(id=user_id)

        message = render_to_string(
            template_name="emails/registration_email.html",
            context={
                "user": user_instance,
                "domain": settings.SITE_DOMAIN,
                "uid": urlsafe_base64_encode(force_bytes(user_instance.pk)),
                "token": TokenGenerator().make_token(user_instance),
            },
        )

        email = EmailMessage(
            subject="Activate your account",
            body=message,
            to=[user_instance.email],
            from_email=settings.EMAIL_HOST_USER,
        )
        email.content_subtype = "html"
        email.send(fail_silently=settings.EMAIL_FAIL_SILENTLY)
    except Exception as e:
        print(f"Error sending email: {e}")
        raise
