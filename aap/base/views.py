"""Base views."""
import uuid

from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets


class BaseViewSet(viewsets.GenericViewSet):
    """Get by multiple lookup fields."""

    # It should be override in the derived classes.
    alternative_lookup_field = None

    def get_object(self):
        if not self.alternative_lookup_field:
            return super().get_object()

        queryset = self.get_queryset()
        try:
            field = "pk"
            value = uuid.UUID(self.kwargs[self.lookup_field]).hex
        except ValueError:
            field = self.alternative_lookup_field
            value = self.kwargs[self.lookup_field]

        if not self.request.user.is_superuser:
            queryset = queryset.filter(user=self.request.user)
        return get_object_or_404(queryset, **{field: value})

    def get_permissions(self):
        """Get permissions based on method."""
        if self.request.method == "GET":
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()
