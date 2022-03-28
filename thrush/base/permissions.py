"""Base permissions."""
from rest_framework import permissions


class ThrushDjangoModelPermissions(permissions.DjangoModelPermissions):
    """Admin Access Point custom model permissions."""

    # DRF default permissions map, except the "GET" one which is customized.
    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": [],
        "HEAD": [],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }
