"""Blog apps config."""
from django.apps import AppConfig
from django.conf import settings

from thrush.apps import all_serializers


class BlogConfig(AppConfig):
    """Blog app config class."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"

    def ready(self):
        settings.SERIALIZERS = all_serializers()
