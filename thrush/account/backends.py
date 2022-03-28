"""Account backends."""
from django.contrib.auth.backends import BaseBackend
from django.db.models import Q

from .models import User


class AccountBackend(BaseBackend):
    """Account authenticate backend."""

    def authenticate(self, request, **kwargs):
        """Authenticate users."""
        user = User.objects.filter(
            Q(mobile=kwargs["username"])
            | Q(username=kwargs["username"])
            | Q(email=kwargs["username"])
        ).first()
        if not user or not user.check_password(kwargs["password"]):
            return None
        return user

