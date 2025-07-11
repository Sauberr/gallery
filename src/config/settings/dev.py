from decouple import config

from config.settings.base import *  # noqa

DEBUG = True

SECRET_KEY = "django-secret-key"

ALLOWED_HOSTS: list[Any] = ["*", "127.0.0.1"]

CORS_ALLOW_ALL_ORIGINS: bool = True
CORS_ALLOW_CREDENTIALS: bool = True

CORS_ALLOW_HEADERS = [
    "authorization",
    "content-type",
    "accept",
]

CORS_ALLOWED_ORIGINS: list[str] = [
    "http://127.0.0.1:8000",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB", default="postgres", cast=str),
        "USER": config("POSTGRES_USER", default="postgres", cast=str),
        "PASSWORD": config("POSTGRES_PASSWORD", default="postgres", cast=str),
        "HOST": config("POSTGRES_HOST", default="localhost", cast=str),
        "PORT": config("POSTGRES_PORT", default=5432, cast=int),
    },
}

BASIC_PLAN_ID = config("BASIC", default="", cast=str)
PREMIUM_PLAN_ID = config("PREMIUM", default="", cast=str)
ENTERPRISE_PLAN_ID = config("ENTERPRISE", default="", cast=str)


STATIC_URL = "/static/"

STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"

STATIC_ROOT = BASE_DIR / "staticfiles"

EMAIL_BACKEND = config("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend", cast=str)
EMAIL_HOST = config("EMAIL_HOST", default="localhost", cast=str)
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="", cast=str)
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="", cast=str)
EMAIL_FAIL_SILENTLY = config("EMAIL_FAIL_SILENTLY", default=False, cast=bool)

RECAPTCHA_PUBLIC_KEY = config("RECAPTCHA_PUBLIC_KEY", default="", cast=str)
RECAPTCHA_PRIVATE_KEY = config("RECAPTCHA_PRIVATE_KEY", default="", cast=str)

CELERY_BEAT_SCHEDULE = {
    "process-expired-subscriptions": {
        "task": "subscriptions.tasks.process_expired_subscriptions",
        "schedule": crontab(minute="*/2"),
    },
    "check-subscriptions-for-notification": {
        "task": "subscriptions.tasks.check_subscriptions_for_notification",
        "schedule": crontab(minute="*/2"),
    },
}
