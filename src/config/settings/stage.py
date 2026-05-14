from typing import Any

from config.settings.base import *  # noqa

DEBUG = False

SECRET_KEY = config("SECRET_KEY")

ALLOWED_HOSTS: list[Any] = config("ALLOWED_HOSTS", default="localhost,127.0.0.1").split(",")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

STATIC_URL = "static/"
