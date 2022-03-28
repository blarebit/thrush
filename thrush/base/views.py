"""Base views."""
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, viewsets

from .models import Category, Tag
from .serializers import CategorySerializer, TagSerializer


class BaseViewSet(viewsets.GenericViewSet):
    """Get by multiple lookup fields."""

    # It should be override in the derived classes.
    alternative_lookup_field = None

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

        if not self.request.user.is_superuser:
            queryset = queryset.filter(user=self.request.user)
        return get_object_or_404(queryset, **{field: value})

    def get_permissions(self):
        """Get permissions based on method."""
        if self.request.method == "GET":
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def get_queryset(self):
        """
        This view should return a list of all the cart
        for the currently authenticated user.
        """
        user = self.request.user
        # breakpoint()
        return self.queryset.filter(user=user)


class TagViewSet(
    BaseViewSet,
    generics.ListCreateAPIView,
    generics.RetrieveAPIView,
    generics.CreateAPIView,
):
    """Tag view set."""

    permission_classes = [permissions.DjangoModelPermissions]
    queryset = Tag.objects.filter(is_deleted=False)
    serializer_class = TagSerializer
    alternative_lookup_field = "name"
    filterset_fields = ("name",)


class CategoryViewSet(
    BaseViewSet, generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView
):
    """Category view set."""

    permission_classes = [permissions.DjangoModelPermissions]
    queryset = Category.objects.filter(is_deleted=False)
    serializer_class = CategorySerializer
    alternative_lookup_field = "name"
    filterset_fields = ("name",)
