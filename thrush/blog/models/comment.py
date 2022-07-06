"""Blog comment models."""
from account.models import User
from base.models import BaseComment, assign_object_permissions
from django.db import models
from .post import Post
from django.dispatch import receiver
from django.db.models.signals import post_save
from guardian.models import UserObjectPermissionBase
from guardian.models import GroupObjectPermissionBase


class Comment(BaseComment):
    """Comment model implementation."""

    model_name = "comment"

    user = models.ForeignKey(
        User, related_name="post_comment_user", on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post, related_name="post_comments", on_delete=models.CASCADE
    )

    class Meta:
        permissions = (("approve_comment", "Can approve comment"),)


class CommentUserObjectPermission(UserObjectPermissionBase):
    """Guardian user object class."""

    content_object = models.ForeignKey(Comment, on_delete=models.CASCADE)


class CommentGroupObjectPermission(GroupObjectPermissionBase):
    """Guardian group object class."""

    content_object = models.ForeignKey(Comment, on_delete=models.CASCADE)


@receiver(post_save, sender=Comment)
def add_permissions(sender, instance, created, **kwargs):
    if created:
        assign_object_permissions(instance, instance.user)
