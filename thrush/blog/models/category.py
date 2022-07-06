"""Blog category models."""
from base.models import Base, assign_object_permissions
from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from guardian.models import UserObjectPermissionBase
from guardian.models import GroupObjectPermissionBase


class Category(Base):
    """Category model implementation."""

    model_name = "category"

    name = models.CharField(max_length=75)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="category_parent",
        on_delete=models.SET_NULL,
    )

    class Meta:
        unique_together = ("name", "parent")

    def __str__(self):
        if self.is_deleted:
            return f"{self.name} [deleted]"
        return self.name


class CategoryUserObjectPermission(UserObjectPermissionBase):
    """Guardian user object class."""

    content_object = models.ForeignKey(Category, on_delete=models.CASCADE)


class CategoryGroupObjectPermission(GroupObjectPermissionBase):
    """Guardian group object class."""

    content_object = models.ForeignKey(Category, on_delete=models.CASCADE)


@receiver(post_save, sender=Category)
def add_permissions(sender, instance, created, **kwargs):
    if created:
        assign_object_permissions(instance)
