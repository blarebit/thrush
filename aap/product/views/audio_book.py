"""Audio book views."""
from base.views import BaseViewSet
from base.models import Product
from product.models import (
    AudioBook,
    AudioIndex,
    AudioType,
    Author,
    Speaker,
    CompatibleDevice,
    Publisher,
)
from product.serializers import (
    AudioBookSerializer,
    AudioIndexSerializer,
    AudioTypeSerializer,
    BookAuthorSerializer,
    BookSpeakerSerializer,
    CompatibleDeviceSerializer,
    PublisherSerializer,
)
from rest_framework import generics, permissions


class AudioTypeViewSet(
    BaseViewSet,
    generics.ListCreateAPIView,
    generics.RetrieveAPIView,
    generics.CreateAPIView,
):
    """Audio type view set."""

    permission_classes = [permissions.DjangoModelPermissions]
    queryset = AudioType.objects.all()
    serializer_class = AudioTypeSerializer
    alternative_lookup_field = "name"
    filterset_fields = ("name",)


class BookSpeakerViewSet(
    BaseViewSet,
    generics.ListCreateAPIView,
    generics.RetrieveAPIView,
    generics.CreateAPIView,
):
    """Book speaker view set."""

    permission_classes = [permissions.DjangoModelPermissions]
    queryset = Speaker.objects.all()
    serializer_class = BookSpeakerSerializer
    alternative_lookup_field = "name"
    filterset_fields = ("name",)


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


class CompatibleDeviceViewSet(
    BaseViewSet,
    generics.ListCreateAPIView,
    generics.RetrieveAPIView,
    generics.CreateAPIView,
):
    """Compatible device view set."""

    permission_classes = [permissions.DjangoModelPermissions]
    queryset = CompatibleDevice.objects.all()
    serializer_class = CompatibleDeviceSerializer
    alternative_lookup_field = "name"
    filterset_fields = ("name", "version")


class AudioIndexViewSet(
    BaseViewSet,
    generics.ListCreateAPIView,
    generics.RetrieveAPIView,
    generics.CreateAPIView,
):
    """Audio index view set."""

    permission_classes = [permissions.DjangoModelPermissions]
    queryset = AudioIndex.objects.all()
    serializer_class = AudioIndexSerializer
    filterset_fields = ("is_downloadable",)


class AudioBookViewSet(
    BaseViewSet,
    generics.ListCreateAPIView,
    generics.RetrieveAPIView,
    generics.CreateAPIView,
):
    """Audio book view set."""

    permission_classes = [permissions.DjangoModelPermissions]
    queryset = AudioBook.objects.all()
    serializer_class = AudioBookSerializer
    alternative_lookup_field = "name"
    filterset_fields = ("name",)
