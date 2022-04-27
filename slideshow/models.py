"""Slideshow app models."""
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models

from base.models import Base


class GroupSlideShow(Base):
    """GroupSlideShow model implementation."""

    name = models.CharField(max_length=50)

    class Meta:
        unique_together = [("is_deleted", "name")]

    def __str__(self):
        return self.name


def get_delete_slide_group():
    """Handle deleting a group slide."""
    return GroupSlideShow.objects.get_or_create(name=settings.DELETED_SLIDE_GROUP_NAME)


class SlideShow(Base):
    """SlideShow model implementation."""

    title = models.CharField(max_length=1024)
    description = models.TextField(null=True, blank=True)
    image = models.CharField(max_length=1024)
    group_slideshow = models.ForeignKey(
        GroupSlideShow, on_delete=models.SET(get_delete_slide_group)
    )
    link_type = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.DO_NOTHING
    )
    link = models.CharField(max_length=1024)
    order = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ["order"]
        unique_together = [("is_deleted", "title")]

    def __str__(self):
        return self.title
