"""Base apps config."""
from django.apps import AppConfig
from django.conf import settings

from aap.apps import all_serializers


class BaseConfig(AppConfig):
    """Base app config class."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "base"

    def ready(self):
        settings.SERIALIZERS = all_serializers()
