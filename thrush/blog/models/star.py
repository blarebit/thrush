"""Blog app models."""
from account.models import User
from base.models import BaseStar, assign_object_permissions
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from .post import Post
from guardian.models import UserObjectPermissionBase
from guardian.models import GroupObjectPermissionBase


class Star(BaseStar):
    """Star (posts) model implementation."""

    model_name = "star"

    user = models.ForeignKey(
        User, related_name="post_star_user", on_delete=models.CASCADE
    )
    post = models.ForeignKey(Post, related_name="post_stars", on_delete=models.CASCADE)

    class Meta:
        unique_together = [("user", "post")]

    def __str__(self):
        return f"{self.post.title}[{self.star}]"


class StarUserObjectPermission(UserObjectPermissionBase):
    """Guardian user object class."""

    content_object = models.ForeignKey(Star, on_delete=models.CASCADE)


class StarGroupObjectPermission(GroupObjectPermissionBase):
    """Guardian group object class."""

    content_object = models.ForeignKey(Star, on_delete=models.CASCADE)


@receiver(post_save, sender=Star)
def add_permissions(sender, instance, created, **kwargs):
    if created:
        assign_object_permissions(instance, instance.user)
