"""Page models."""
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models

from base.models import Base


class Page(Base):
    """Page model."""

    title = models.CharField(max_length=255, unique=True)
    content = models.TextField()


class GroupMenu(Base):
    """Group menu model implementation."""

    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=150, blank=True, null=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


def get_delete_menu_group():
    """Handle deleting a group menu."""
    return GroupMenu.objects.get_or_create(name=settings.DELETED_MENU_GROUP_NAME)


class Menu(Base):
    """Menu model implementation."""

    label = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=150, blank=True, null=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    group_menu = models.ForeignKey(
        GroupMenu, on_delete=models.SET(get_delete_menu_group)
    )
    link_type = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.DO_NOTHING
    )
    link = models.CharField(max_length=1024)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.label
