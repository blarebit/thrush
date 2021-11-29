"""
Django settings for aap project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import ast
import os
from ast import literal_eval
from pathlib import Path

from django.core.validators import get_available_image_extensions

from .apps import all_serializers

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "AAP_SECRET_KEY",
    "django-insecure-&yt8!+ph$6sy+%jq+p-f$=^xz1w%xunu7f4)a7zg&(-+&@sxd0",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = literal_eval(os.environ.get("AAP_DEBUG", "True"))

ALLOWED_HOSTS = literal_eval(
    os.environ.get("AAP_ALLOWED_HOSTS", "['localhost', '127.0.0.1']")
)

CORS_ALLOWED_HOST = os.environ.get("AAP_CORS_ALLOWED_HOST", "*")

# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "drf_yasg",
    "account",
    "blog",
    "page",
    "file",
    "slideshow",
]

# Note: it will be overridden by 'page' app.
SERIALIZERS = {}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "aap.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
]

ROOT_URLCONF = "aap.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "aap.wsgi.application"

APPEND_SLASH = True

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}
}

# Customized models.

AUTH_USER_MODEL = "account.User"
MOBILE_LENGTH = int(os.environ.get("AAP_MOBILE_LENGTH", "13"))

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTHENTICATION_BACKENDS = [
    "account.backends.AccountBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = os.environ.get("AAP_TIME_ZONE", "UTC")
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

# Media files and directories.

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_ALLOWED_EXTENSIONS = ast.literal_eval(
    os.environ.get(
        "AAP_MEDIA_ALLOWED_EXTENSIONS", str(get_available_image_extensions())
    )
)

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# DRF settings.

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": int(os.environ.get("AAP_PAGE_SIZE", 10)),
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

# Swagger settings.

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Basic": {"type": "basic"},
        "DRF Token": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
        },
    }
}

# Account component settings.

DEFAULT_USER_GROUP = "users"
LOGIN_URL = "/account/login"
LOGOUT_URL = "/account/logout"

# Blog component settings.

STAR_MIN_VALUE = int(os.environ.get("AAP_STAR_MIN_VALUE", "1"))
STAR_MAX_VALUE = int(os.environ.get("AAP_STAR_MAX_VALUE", "10"))

# Set Default value for "category" field in "post" table when
# category record deleted in "category" table.
DELETED_POST_CATEGORY_NAME = "__deleted_category"

# Page component settings.

DELETED_MENU_GROUP_NAME = "__deleted_group_menu"

# Slideshow component settings.

DELETED_SLIDE_GROUP_NAME = "__deleted_group_menu"
