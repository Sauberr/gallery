from typing import Any

from config.settings.base import *  # noqa

DEBUG = False

SECRET_KEY = "django-secret-key"

ALLOWED_HOSTS: list[Any] = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

STATIC_URL = "static/"
