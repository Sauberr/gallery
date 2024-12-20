from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from core.utils.token_generator import TokenGenerator


from celery import shared_task


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
            from_email=settings.EMAIL_HOST_USER
        )
        email.content_subtype = "html"
        email.send(fail_silently=False)  # Измените на False для отладки
    except Exception as e:
        print(f"Error sending email: {e}")  # Для отладки
        raise