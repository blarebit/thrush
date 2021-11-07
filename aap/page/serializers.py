"""Page serializers."""
from rest_framework import serializers

from .models import GroupMenu, Menu, Page


class PageSerializer(serializers.ModelSerializer):
    """Page serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="page:page-detail")

    class Meta:
        model = Page
        fields = "__all__"


class MenuSerializer(serializers.ModelSerializer):
    """Menu serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="page:menu-detail")

    class Meta:
        model = Menu
        fields = "__all__"


class GroupMenuSerializer(serializers.ModelSerializer):
    """Group menu serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="page:group_menu-detail")
    menus = MenuSerializer(source="menu_set", many=True, read_only=True)

    class Meta:
        model = GroupMenu
        fields = "__all__"
