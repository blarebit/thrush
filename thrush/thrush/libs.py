"""Thrush libraries."""
from django.conf import settings


class DatabaseRouter:
    """Database router."""

    def db_for_read(self, model, **hints):
        """Read database."""
        return settings.ENVIRONMENT

    def db_for_write(self, model, **hints):
        """Write database."""
        return settings.ENVIRONMENT

    def allow_relation(self, obj1, obj2, **hints):
        """Allow relation between two objects."""
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Allow migrations."""
        return True
