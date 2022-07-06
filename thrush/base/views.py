"""Base views."""
from typing import Any, Dict, Optional

from rest_framework_nested.viewsets import NestedViewSetMixin
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets


class BaseViewSet(viewsets.GenericViewSet, NestedViewSetMixin):
    """Get by multiple lookup fields."""

    # It should be overridden in the derived classes.
    alternative_lookup_field: Optional[str] = None
    # Filter data based on field name and kwargs values, e.g. {"post": "post_pk"}
    filter_by_fields: Dict[str, str] = {}
    # Filter data based on permission code and query, e.g. {"blog.approve_comment": {"is_approve": None}}
    # If the query contains None, it means remove the field from the query.
    filter_by_permissions: Dict[str, Dict[str, Any]] = {}

    def get_object(self):
        """DRF built-in method.

        Implement "alternative lookup field" feature.
        """
        if not self.alternative_lookup_field:
            return super().get_object()

        queryset = self.get_queryset()
        if self.kwargs[self.lookup_field].isdigit():
            field = "pk"
            value = self.kwargs[self.lookup_field].isdigit()
        else:
            field = self.alternative_lookup_field
            value = self.kwargs[self.lookup_field]

        if hasattr(queryset.model, "user"):
            if not self.request.user.is_superuser:
                queryset = queryset.filter(user=self.request.user)
        return get_object_or_404(queryset, **{field: value})

    def get_permissions(self):
        """Get permissions based on method."""
        if self.request.method == "GET":
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def get_queryset(self):
        """Basic queryset to automatically filter based on filter_by_fields."""
        if not self.filter_by_fields or getattr(self, "swagger_fake_view", False):
            return super().get_queryset()

        filter_items = {}
        for key, value in self.filter_by_fields.items():
            filter_items[key] = self.kwargs[value]

        # for permission_code, filter_conditions in self.filter_by_permissions.items():
            # if self.request.user.has_perm(permission_code):
                # for key, value in filter_conditions.items():
                    # if value is None and key in filter_items:
                        # del filter_items[key]
                    # else:
                        # filter_items[key] = value

        return super().get_queryset().filter(**filter_items)
