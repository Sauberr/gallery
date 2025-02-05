from config.settings.base import *  # noqa


DEBUG = True

SECRET_KEY = "django-secret-key"

ALLOWED_HOSTS: List[Any] = ["*", "127.0.0.1"]


# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": str(os.environ.get("POSTGRES_DB")),
        "USER": str(os.environ.get("POSTGRES_USER")),
        "PASSWORD": str(os.environ.get("POSTGRES_PASSWORD")),
        "HOST": str(os.environ.get("POSTGRES_HOST")),
        "PORT": int(os.environ.get("POSTGRES_PORT")),
    },
}

BASIC_PLAN_ID = os.environ.get('BASIC')
PREMIUM_PLAN_ID = os.environ.get('PREMIUM')
ENTERPRISE_PLAN_ID = os.environ.get('ENTERPRISE')


STATIC_URL = "/static/"

STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"

STATIC_ROOT = BASE_DIR / "staticfiles"

EMAIL_BACKEND = str(os.environ.get("EMAIL_BACKEND"))
EMAIL_HOST = str(os.environ.get("EMAIL_HOST"))
EMAIL_PORT = str(os.environ.get("EMAIL_PORT"))
EMAIL_USE_TLS = bool(os.environ.get("EMAIL_USE_TLS"))
EMAIL_HOST_USER = str(os.environ.get("EMAIL_HOST_USER"))
EMAIL_HOST_PASSWORD = str(os.environ.get("EMAIL_HOST_PASSWORD"))
EMAIL_FAIL_SILENTLY = bool(os.environ.get("EMAIL_FAIL_SILENTLY"))

RECAPTCHA_PUBLIC_KEY = str(os.environ.get("RECAPTCHA_PUBLIC_KEY"))
RECAPTCHA_PRIVATE_KEY = str(os.environ.get("RECAPTCHA_PRIVATE_KEY"))
