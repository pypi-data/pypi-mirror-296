"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path

from khoj.utils.helpers import in_debug_mode, is_env_var_true

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("KHOJ_DJANGO_SECRET_KEY", "!secret")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = in_debug_mode()

# All Subdomains of KHOJ_DOMAIN are trusted
KHOJ_DOMAIN = os.getenv("KHOJ_DOMAIN", "khoj.dev")
ALLOWED_HOSTS = [f".{KHOJ_DOMAIN}", "localhost", "127.0.0.1", "[::1]", f"{KHOJ_DOMAIN}"]

CSRF_TRUSTED_ORIGINS = [
    f"https://*.{KHOJ_DOMAIN}",
    f"https://{KHOJ_DOMAIN}",
    f"http://*.{KHOJ_DOMAIN}",
    f"http://{KHOJ_DOMAIN}",
    f"https://app.{KHOJ_DOMAIN}",
]

DISABLE_HTTPS = is_env_var_true("KHOJ_NO_HTTPS")

COOKIE_SAMESITE = "None"
if DEBUG or os.getenv("KHOJ_DOMAIN") == None:
    SESSION_COOKIE_DOMAIN = "localhost"
    CSRF_COOKIE_DOMAIN = "localhost"
else:
    # Production Settings
    SESSION_COOKIE_DOMAIN = KHOJ_DOMAIN
    CSRF_COOKIE_DOMAIN = KHOJ_DOMAIN
    if not DISABLE_HTTPS:
        SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

if DISABLE_HTTPS:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

    # These need to be set to Lax in order to work with http in some browsers. See reference: https://docs.djangoproject.com/en/5.0/ref/settings/#std-setting-SESSION_COOKIE_SECURE
    COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SAMESITE = "Lax"
else:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    COOKIE_SAMESITE = "None"
    SESSION_COOKIE_SAMESITE = "None"

# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "khoj.database.apps.DatabaseConfig",
    "django.contrib.admin",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "phonenumber_field",
    "django_apscheduler",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "khoj.app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "DIRS": [os.path.join(BASE_DIR, "templates"), os.path.join(BASE_DIR, "templates", "account")],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

ASGI_APPLICATION = "app.asgi.application"

CLOSE_CONNECTIONS_AFTER_REQUEST = True

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATA_UPLOAD_MAX_NUMBER_FIELDS = 20000
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
        "USER": os.getenv("POSTGRES_USER", "postgres"),
        "NAME": os.getenv("POSTGRES_DB", "khoj"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres"),
        "CONN_MAX_AGE": 0,
        "CONN_HEALTH_CHECKS": True,
    }
}

# User Settings
AUTH_USER_MODEL = "database.KhojUser"

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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = [
    BASE_DIR / "interface/web",
    BASE_DIR / "interface/email",
    BASE_DIR / "interface/built",
    BASE_DIR / "interface/compiled",
]
STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Format string for displaying run time timestamps in the Django admin site. The default
# just adds seconds to the standard Django format, which is useful for displaying the timestamps
# for jobs that are scheduled to run on intervals of less than one minute.
#
# See https://docs.djangoproject.com/en/dev/ref/settings/#datetime-format for format string
# syntax details.
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"

# Maximum run time allowed for jobs that are triggered manually via the Django admin site, which
# prevents admin site HTTP requests from timing out.
#
# Longer running jobs should probably be handed over to a background task processing library
# that supports multiple background worker processes instead (e.g. Dramatiq, Celery, Django-RQ,
# etc. See: https://djangopackages.org/grids/g/workers-queues-tasks/ for popular options).
APSCHEDULER_RUN_NOW_TIMEOUT = 240  # Seconds
