from celery.schedules import crontab
from decouple import config

from config.settings.base import *  # noqa

DEBUG = True

INSTALLED_APPS = INSTALLED_APPS + ("debug_toolbar",)  # type: ignore[operator]
MIDDLEWARE = list(MIDDLEWARE)  # type: ignore[arg-type]
MIDDLEWARE.insert(
    MIDDLEWARE.index("django_prometheus.middleware.PrometheusAfterMiddleware"),
    "debug_toolbar.middleware.DebugToolbarMiddleware",
)
MIDDLEWARE = tuple(MIDDLEWARE)

DEBUG_TOOLBAR_PANELS: list[str] = [
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.logging.LoggingPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
    "cachalot.panels.CachalotPanel",
]

SECRET_KEY = "django-secret-key"

ALLOWED_HOSTS: list = ["*", "127.0.0.1"]

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

RECAPTCHA_PUBLIC_KEY = config("RECAPTCHA_PUBLIC_KEY", default="6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI", cast=str)
RECAPTCHA_PRIVATE_KEY = config("RECAPTCHA_PRIVATE_KEY", default="6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe", cast=str)
SILENCED_SYSTEM_CHECKS = ["django_recaptcha.recaptcha_test_key_error"]

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
