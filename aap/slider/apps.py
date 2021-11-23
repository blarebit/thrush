"""Slider apps config."""
from django.apps import AppConfig
from django.conf import settings

from aap.apps import all_serializers


class SliderConfig(AppConfig):
    """Slider app config class."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "slider"

    def ready(self):
        settings.SERIALIZERS = all_serializers()
