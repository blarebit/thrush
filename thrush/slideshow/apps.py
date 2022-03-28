"""SlideShow apps config."""
from django.apps import AppConfig
from django.conf import settings

from aap.apps import all_serializers


class SlideShowConfig(AppConfig):
    """SlideShow app config class."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "slideshow"

    def ready(self):
        """Slideshow ready."""
        settings.SERIALIZERS = all_serializers()
