"""Audio book views."""
from base.views import BaseViewSet
# from base.models import Product
from product.models import (
    # AudioBook,
    # AudioIndex,
    # AudioType,
    Author,
    # Speaker,
    # CompatibleDevice,
    Publisher,
    PaperBook
)
from product.serializers import (
    AudioBookSerializer,
    AudioIndexSerializer,
    AudioTypeSerializer,
    BookAuthorSerializer,
    BookSpeakerSerializer,
    CompatibleDeviceSerializer,
    PublisherSerializer,
    PaperBookSerializer
)
from rest_framework import generics, permissions


class BookAuthorViewSet(
    BaseViewSet,
    generics.ListCreateAPIView,
    generics.RetrieveAPIView,
    generics.CreateAPIView,
):
    """Book author view set."""

    permission_classes = [permissions.DjangoModelPermissions]
    queryset = Author.objects.all()
    serializer_class = BookAuthorSerializer
    alternative_lookup_field = "name"
    filterset_fields = ("name",)


class PublisherViewSet(
    BaseViewSet,
    generics.ListCreateAPIView,
    generics.RetrieveAPIView,
    generics.CreateAPIView,
):
    """Publisher view set."""

    permission_classes = [permissions.DjangoModelPermissions]
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    alternative_lookup_field = "name"
    filterset_fields = ("name",)


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

