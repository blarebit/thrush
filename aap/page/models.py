"""Page models."""
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models

from base.models import Base, BaseManager


class Page(Base):
    """Page model."""

    title = models.CharField(max_length=255, unique=True)
    content = models.TextField()


class GroupMenu(Base):
    """Group menu model."""

    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=150, blank=True, null=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    order = models.PositiveIntegerField(default=1)


def get_delete_menu_group():
    """Handle deleting a group menu."""
    return GroupMenu.objects.get_or_create(name=settings.DELETED_MENU_GROUP_NAME)


class MenuManager(BaseManager):
    """Menu model manager."""

    def get_queryset(self):
        """Django built-in method.

        Convert the 'link' value into an object based on the 'link_type' field.
        """
        queryset = super().get_queryset()
        for query in queryset:
            if query.link_type:
                model = query.link_type.model_class()
                try:
                    query.link = model.objects.get(id=query.link)
                except model.DoesNotExist:
                    continue
        return queryset


class Menu(Base):
    """Menu model."""

    label = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=150, blank=True, null=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    group_menu = models.ForeignKey(GroupMenu, on_delete=models.SET(get_delete_menu_group))
    link_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.DO_NOTHING)
    link = models.CharField(max_length=1024)

    objects = MenuManager()
