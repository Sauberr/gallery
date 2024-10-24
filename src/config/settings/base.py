import os
from pathlib import Path
from typing import Tuple, List, Any
import sentry_sdk

from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-x*l7&fx$1@@z)fol=kj4fl6d5gg6ou$+1%x823644xoyw09d2%'


ALLOWED_HOSTS: List[Any] = ["*", "127.0.0.1", "localhost"]

INTERNAL_IPS: List[str] = [
    "127.0.0.1",
]

# Application definition

INSTALLED_APPS: Tuple[str, ...] = (

    # Django apps
    "jet.dashboard",
    "jet",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_prometheus",
    "django_extensions",
    "rest_framework",
    "django_elasticsearch_dsl",
    "django.contrib.humanize",
    "debug_toolbar",

    # Custom apps
    "phonenumber_field",
    "crispy_forms",
    "crispy_bootstrap5",
    "django_inlinecss",
    "django_recaptcha",
    "drf_yasg",
    "social_django",

    # My apps
    "core",
    "subscriptions",
    "account",
    "api",
    "images",
)

CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE: Tuple[str, ...] = (
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
)

ROOT_URLCONF: str = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


sentry_sdk.init(
    dsn="https://e234bbcf9adac056b2fd1709d2727d16@o4507838166466560.ingest.de.sentry.io/4507838177542224",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


AUTH_USER_MODEL: str = "account.User"

LOGIN_URL: str = "account:login"
LOGIN_REDIRECT_URL: str = "core:index"
LOGOUT_REDIRECT_URL: str = "core:index"


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'http://elasticsearch:9200'
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


SECURE_CROSS_ORIGIN_OPENER_POLICY: str = 'same-origin-allow-popups'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


SOCIAL_AUTH_URL_NAMESPACE: str = "social"


AUTHENTICATION_BACKENDS: List[str] = [
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'account.auth_backend.AuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")

SOCIAL_AUTH_GITHUB_KEY = 'Ov23lituVCnvAs80C47d'
SOCIAL_AUTH_GITHUB_SECRET = 'ae37c4070d47038ceacb6c90c00e4af48d509697'

SOCIAL_AUTH_PIPELINE: Tuple[str, ...] = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'account.pipeline.cleanup_social_account',
    'account.pipeline.activate_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details'
)

JET_THEMES = [
    {"theme": "default", "color": "#47bac1", "title": "Default"},
    {"theme": "green", "color": "#44b78b", "title": "Green"},
    {"theme": "light-green", "color": "#2faa60", "title": "Light Green"},
    {"theme": "light-violet", "color": "#a464c4", "title": "Light Violet"},
    {"theme": "light-blue", "color": "#5EADDE", "title": "Light Blue"},
    {"theme": "light-gray", "color": "#222", "title": "Light Gray"},
]

REST_FRAMEWORK = {"DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"]}