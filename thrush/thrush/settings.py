"""
Django settings for aap project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import ast
import math
import os
from ast import literal_eval
from pathlib import Path

from cryptography.fernet import Fernet
from django.core.validators import get_available_image_extensions

from .apps import all_serializers

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# General

ENVIRONMENT = os.environ.get("THRUSH_ENVIRONMENT")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "AAP_SECRET_KEY",
    "django-insecure-&yt8!+ph$6sy+%jq+p-f$=^xz1w%xunu7f4)a7zg&(-+&@sxd0",
)
CRYPTOGRAPHY = Fernet(
    os.environ.get(
        "AAP_CRYPTOGRAPHY_KEY", "oeCpvSkfcN5qhKttyqg1GJrZCoEQ4p6ZWPh1T3QuDNk="
    )
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = literal_eval(os.environ.get("THRUSH_DEBUG", "True"))

ALLOWED_HOSTS = literal_eval(
    os.environ.get("THRUSH_ALLOWED_HOSTS", "['localhost', '127.0.0.1']")
)
CORS_ALLOWED_ORIGIN_REGEXES = [
    "http(s)?://.*",
]

FIRST_DAY_OF_WEEK = int(os.environ.get("THRUSH_FIRST_DAY_OF_WEEK", "0"))
IGNORABLE_404_URLS = ["favicon.ico"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "polymorphic",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "django_filters",
    "drf_yasg",
    "account",
    "base",
    "blog",
    # "page",
    # "file",
    # "slideshow",
    # "shop.cart",
    # "shop.product",
    # "shop.payment",
]

# Note: it will be overridden by 'page' app.
SERIALIZERS = {}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
]

ROOT_URLCONF = "thrush.urls"

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

WSGI_APPLICATION = "thrush.wsgi.application"

APPEND_SLASH = True

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
    "production": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("THRUSH_DATABASES_PRODUCTION_HOST", "127.0.0.1"),
        "PORT": int(os.environ.get("THRUSH_DATABASES_PRODUCTION_PORT", "5432")),
        "NAME": "thrush",
        "USER": os.environ.get("THRUSH_DATABASES_PRODUCTION_USER", "postgres"),
        "PASSWORD": os.environ.get("THRUSH_DATABASES_PRODUCTION_PASSWORD", "postgres"),
    },
}

DATABASE_ROUTERS = ["thrush.libs.DatabaseRouter"]

# Cache
# https://docs.djangoproject.com/en/4.0/topics/cache/

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.environ.get("THRUSH_REDIS", "redis://127.0.0.1:6379"),
    },
}

# Email
# https://docs.djangoproject.com/en/4.0/topics/email/

# # Server
EMAIL_HOST = os.environ.get("THRUSH_EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("THRUSH_EMAIL_PORT", "25"))
EMAIL_HOST_USER = os.environ.get("THRUSH_EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("THRUSH_EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = literal_eval(os.environ.get("THRUSH_EMAIL_USE_TLS", "True"))
EMAIL_USE_SSL = literal_eval(os.environ.get("THRUSH_EMAIL_USE_SSL", "True"))
EMAIL_TIMEOUT = int(os.environ.get("THRUSH_EMAIL_TIMEOUT", "0"))
EMAIL_USE_LOCALTIME = literal_eval(
    os.environ.get("THRUSH_EMAIL_USE_LOCALTIME", "False")
)

# # General
EMAIL_SUBJECT_PREFIX = os.environ.get("THRUSH_EMAIL_SUBJECT_PREFIX", "")
DEFAULT_FROM_EMAIL = os.environ.get("THRUSH_DEFAULT_FROM_EMAIL", "")
SERVER_EMAIL = os.environ.get("THRUSH_SERVER_EMAIL", "")

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
TIME_ZONE = os.environ.get("THRUSH_TIME_ZONE", "UTC")
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = os.environ.get("THRUSH_STATIC_URL", "/static/")
STATIC_ROOT = BASE_DIR / "static"

# Media files and directories.

MEDIA_URL = os.environ.get("THRUSH_MEDIA_URL", "/media/")
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_ALLOWED_EXTENSIONS = ast.literal_eval(
    os.environ.get(
        "THRUSH_MEDIA_ALLOWED_EXTENSIONS", str(get_available_image_extensions())
    )
)

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# DRF settings

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": int(os.environ.get("THRUSH_PAGE_SIZE", 10)),
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
}

# Swagger settings

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

# Account component

AUTH_USER_MODEL = "account.User"
DEFAULT_USER_GROUP = "registered_users"
DEFAULT_USER_GROUP_PERMISSIONS = [
    # Tag
    "blog.tag.view",
    "blog.tag.add",
    # Category
    "blog.category.view",
    "blog.category.add",
    "blog.category.change",
    # Post
    "blog.post.view",
    "blog.post.add",
    "blog.post.change",
    "blog.post.delete",
]
MOBILE_LENGTH = int(os.environ.get("THRUSH_MOBILE_LENGTH", "13"))
VERIFICATION_CODE_LENGTH = int(os.environ.get("THRUSH_VERIFY_CODE_LENGTH", "6"))
VERIFICATION_CODE_LENGTH_RANGE = (
    math.pow(10, VERIFICATION_CODE_LENGTH - 1),
    math.pow(10, VERIFICATION_CODE_LENGTH) - 1,
)
VERIFICATION_CODE_LIFE_TIME = int(
    os.environ.get("THRUSH_VERIFY_CODE_LIFE_TIME", 60 * 3)
)
LOGIN_URL = "/account/login"
LOGOUT_URL = "/account/logout"

# Blog component

STAR_MIN_VALUE = int(os.environ.get("THRUSH_STAR_MIN_VALUE", "1"))
STAR_MAX_VALUE = int(os.environ.get("THRUSH_STAR_MAX_VALUE", "10"))

# Set Default value for "category" field in "post" table when
# category record deleted in "category" table.
DELETED_POST_CATEGORY_NAME = "__deleted_category"

# Page component

DELETED_MENU_GROUP_NAME = "__deleted_group_menu"

# Slideshow component

DELETED_SLIDE_GROUP_NAME = "__deleted_group_menu"

# Product component

DELETED_PRODUCT_CATEGORY_NAME = "__deleted_product"
