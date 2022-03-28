"""Apps data."""
import importlib
from typing import Dict

from rest_framework.serializers import Serializer
from django.apps import apps


_ignore_apps = (
    "auth",
    "contenttypes",
    "sessions",
    "staticfiles",
    "rest_framework",
    "authtoken",
    "drf_yasg",
)


def all_serializers() -> Dict[str, Serializer]:
    """Import all serializers and return them.

    Returns:
        Dict[str, Serializer]: imported serializers.
    """
    serializers = {}
    for app in apps.all_models.keys():
        if app in _ignore_apps:
            continue

        try:
            imp = importlib.import_module(f"{app}.serializers")
        except ImportError:
            continue

        for attr, obj in vars(imp).items():
            if attr.endswith("Serializer"):
                serializers[attr] = obj

    return serializers
