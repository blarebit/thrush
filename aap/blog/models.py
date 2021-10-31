"""Blog app models."""
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from base.models import Base, AbstractBase


class Tag(Base):
    """Tag model implementation."""

    name = models.CharField(max_length=75, unique=True)

    def __str__(self):
        if self.is_deleted:
            return f"{self.name} [deleted]"
        return self.name


class Category(Base):
    """Category model implementation."""

    name = models.CharField(max_length=75)
    parent = models.ForeignKey(
        "self",
        null=True,
        related_name="category_parent",
        blank=True,
        on_delete=models.DO_NOTHING,
    )

    def __str__(self):
        if self.is_deleted:
            return f"{self.name} [deleted]"
        return self.name


def get_deleted_post_category():
    """Retrieve or create a category with DELETED_POST_CATEGORY_NAME."""
    return Category.objects.get_or_create(name=settings.DELETED_POST_CATEGORY_NAME)


class Post(Base):
    """Post model implementation."""

    title = models.CharField(max_length=1024, null=False, unique=True)
    brief = models.TextField(null=False)
    content = models.TextField(null=False)
    slug = models.CharField(max_length=1024, unique=True)
    tags = models.ManyToManyField(Tag, related_name="tags")
    bookmarks = models.ManyToManyField(User, related_name="bookmarks", null=True)
    image = models.URLField()
    is_draft = models.BooleanField(default=False)
    previous = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.DO_NOTHING
    )
    user = models.ForeignKey(User, related_name="publisher", on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET(get_deleted_post_category),
    )
    visited = models.PositiveIntegerField(default=0)

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


class Comment(Base):
    """Comment model implementation."""

    user = models.ForeignKey(
        User, related_name="comment_user", on_delete=models.CASCADE
    )
    message = models.CharField(max_length=500)
    reply_to = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, default=""
    )
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        if self.is_deleted:
            return f"{self.message} [deleted]"
        return self.message


class Star(AbstractBase):
    """Star (posts) model implementation."""

    star = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(settings.STAR_MIN_VALUE),
            MaxValueValidator(settings.STAR_MAX_VALUE),
        ]
    )
    user = models.ForeignKey(User, related_name="star_user", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="stars", on_delete=models.CASCADE)

    class Meta:
        ordering = ["created_at"]
        unique_together = [("user", "post")]

    def __str__(self):
        return f"{self.post.title}[{self.star}]"
