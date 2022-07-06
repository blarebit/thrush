"""Blog app models."""
from base.models import Base, assign_object_permissions
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from guardian.models import UserObjectPermissionBase
from guardian.models import GroupObjectPermissionBase


class Tag(Base):
    """Tag model implementation."""

    model_name = "tag"

    name = models.CharField(max_length=75, unique=True)

    def __str__(self):
        if self.is_deleted:
            return f"{self.name} [deleted]"
        return self.name


class TagUserObjectPermission(UserObjectPermissionBase):
    """Guardian user object class."""

    content_object = models.ForeignKey(Tag, on_delete=models.CASCADE)


class TagGroupObjectPermission(GroupObjectPermissionBase):
    """Guardian group object class."""

    content_object = models.ForeignKey(Tag, on_delete=models.CASCADE)


@receiver(post_save, sender=Tag)
def add_permissions(sender, instance, created, **kwargs):
    if created:
        assign_object_permissions(instance)
