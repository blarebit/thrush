"""Blog app models."""
from account.models import User
from base.models import Base, assign_object_permissions
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from .tag import Tag
from .category import Category
from guardian.models import UserObjectPermissionBase
from guardian.models import GroupObjectPermissionBase


def get_deleted_post_category():
    """Retrieve or create a category with DELETED_POST_CATEGORY_NAME."""
    return Category.objects.get_or_create(name=settings.DELETED_POST_CATEGORY_NAME)


class Post(Base):
    """Post model implementation."""

    model_name = "post"

    title = models.CharField(max_length=1024, null=False)
    brief = models.TextField(null=False)
    content = models.TextField(null=False)
    slug = models.CharField(max_length=1024, unique=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="tags")
    bookmarks = models.ManyToManyField(User, related_name="post_bookmarks")
    image = models.URLField()
    is_draft = models.BooleanField(default=False)
    previous = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.DO_NOTHING
    )
    user = models.ForeignKey(User, related_name="post_user", on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET(get_deleted_post_category),
    )
    visited = models.PositiveIntegerField(default=0)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        if self.is_deleted:
            return f"{self.title} [deleted]"
        if self.is_draft:
            return f"{self.title} [draft]"
        if self.previous:
            return f"{self.title} [continue]"
        return self.title


class PostUserObjectPermission(UserObjectPermissionBase):
    """Guardian user object class."""

    content_object = models.ForeignKey(Post, on_delete=models.CASCADE)


class PostGroupObjectPermission(GroupObjectPermissionBase):
    """Guardian group object class."""

    content_object = models.ForeignKey(Post, on_delete=models.CASCADE)


@receiver(post_save, sender=Post)
def add_permissions(sender, instance, created, **kwargs):
    if created:
        assign_object_permissions(instance, instance.user)
