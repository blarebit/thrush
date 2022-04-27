"""Page serializers."""
from rest_framework import serializers

from base.serializers import ContentTypeLinkModelSerializer
from .models import GroupMenu, Menu, Page


class PageSerializer(serializers.ModelSerializer):
    """Page serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="page:page-detail")

    class Meta:
        model = Page
        exclude = ("is_deleted",)


class MenuSerializer(ContentTypeLinkModelSerializer):
    """Menu serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="page:menu-detail")

    class Meta:
        model = Menu
        exclude = ("is_deleted",)


class GroupMenuSerializer(serializers.ModelSerializer):
    """Group menu serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="page:group_menu-detail")
    menus = MenuSerializer(source="menu_set", many=True, read_only=True)

    class Meta:
        model = GroupMenu
        exclude = ("is_deleted",)
