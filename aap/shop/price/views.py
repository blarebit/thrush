"""Price views."""
from base.views import BaseViewSet
from django_filters import rest_framework as filters
from rest_framework import generics, permissions

from .models import Price
from .serializers import PriceSerializer


class PriceFilterSet(filters.FilterSet):
    """Price filter set."""

    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    min_discount = filters.NumberFilter(field_name="discount", lookup_expr="gte")
    max_discount = filters.NumberFilter(field_name="discount", lookup_expr="lte")

    class Meta:
        model = Price
        fields = ("min_price", "max_price", "min_discount", "max_discount", "inventory")


class PriceViewSet(
    BaseViewSet,
    generics.ListCreateAPIView,
    generics.RetrieveAPIView,
    generics.CreateAPIView,
):
    """Price view set."""

    permission_classes = [permissions.DjangoModelPermissions]
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    filterset_class = PriceFilterSet
