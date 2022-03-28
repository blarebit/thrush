"""Account apps config."""
from django.apps import AppConfig


class AuthConfig(AppConfig):
    """Django built-in class."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "account"

    def ready(self):
        """Add 'external' content type."""
        # from django.contrib.contenttypes.models import ContentType

        # ContentType.objects.get_or_create(app_label="external", model="")
