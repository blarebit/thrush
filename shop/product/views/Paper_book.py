"""Audio book views."""
from base.views import BaseViewSet
# from base.models import Product
from shop.product.models import (
    # AudioBook,
    # AudioIndex,
    # AudioType,
    Author,
    # Speaker,
    # CompatibleDevice,
    Publisher,
    PaperBook
)
from shop.product.serializers import (
    # AudioBookSerializer,
    # AudioIndexSerializer,
    # AudioTypeSerializer,
    # BookAuthorSerializer,
    # BookSpeakerSerializer,
    # CompatibleDeviceSerializer,
    # PublisherSerializer,
    PaperBookSerializer
)
from rest_framework import generics, permissions


class PaperBookViewSet(
    BaseViewSet,
    generics.ListCreateAPIView,
    generics.RetrieveAPIView,
    generics.CreateAPIView,
):
    """Paper book view set."""

    permission_classes = [permissions.DjangoModelPermissions]
    queryset = PaperBook.objects.all()
    serializer_class = PaperBookSerializer
    alternative_lookup_field = "name"
    filterset_fields = ("name",)

