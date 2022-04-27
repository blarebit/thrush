"""Blog app models."""
from account.models import User
from base.models import Base, BaseComment, BaseStar
from django.conf import settings
from django.db import models


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
        blank=True,
        related_name="category_parent",
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        unique_together = ("name", "parent")

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


class Comment(BaseComment):
    """Comment model implementation."""

    user = models.ForeignKey(
        User, related_name="post_comment_user", on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post, related_name="post_comments", on_delete=models.CASCADE
    )


class Star(BaseStar):
    """Star (posts) model implementation."""

    user = models.ForeignKey(
        User, related_name="post_star_user", on_delete=models.CASCADE
    )
    post = models.ForeignKey(Post, related_name="post_stars", on_delete=models.CASCADE)

    class Meta:
        unique_together = [("user", "post")]

    def __str__(self):
        return f"{self.post.title}[{self.star}]"
