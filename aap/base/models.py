"""Base apps models."""
import uuid

# from django.utils import timezone
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# from account.models import User
from polymorphic.models import PolymorphicModel


class BaseManager(models.Manager):
    """Base model manager."""

    def get_queryset(self):
        """Django built-in method.

        Filter by is_deleted field.
        """
        return super().get_queryset().filter(is_deleted=False)


class AbstractBase(models.Model):
    """Abstract base model implementation."""

    id = models.UUIDField(  # noqa: A003
        primary_key=True, default=uuid.uuid4, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["created_at"]

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id} {self.created_at}>"


class Base(AbstractBase):
    """Base model implementation."""

    is_deleted = models.BooleanField(default=False)

    objects = BaseManager()

    class Meta:
        abstract = True
        ordering = ["created_at"]

    def delete(self, *args, **kwargs):
        """Django built-in method."""
        self.is_deleted = True
        self.save()

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} {self.id} {self.created_at} {self.is_deleted}>"
        )


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


class BaseComment(Base):
    """Comment model implementation."""

    # user = models.ForeignKey(
    #     User, related_name="comment_user", on_delete=models.CASCADE
    # )
    message = models.CharField(max_length=500)
    reply_to = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, default=""
    )
    # post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ["created_at"]

    def __str__(self):
        if self.is_deleted:
            return f"{self.message} [deleted]"
        return self.message


class BaseStar(AbstractBase):
    """Star (posts) model implementation."""

    star = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(settings.STAR_MIN_VALUE),
            MaxValueValidator(settings.STAR_MAX_VALUE),
        ]
    )
    # user = models.ForeignKey(User, related_name="star_user", on_delete=models.CASCADE)
    # post = models.ForeignKey(Post, related_name="stars", on_delete=models.CASCADE)

    class Meta:
        abstract = True
        ordering = ["created_at"]
        # unique_together = [("user", "post")]

    # def __str__(self):
    #     return f"{self.post.title}[{self.star}]"


class Publisher(Base):
    """Publisher model."""

    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        if self.is_deleted:
            return f"{self.name} [deleted]"
        return self.name


class Author(models.Model):
    """Book author model."""

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Translator(models.Model):
    """Book author model."""

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Speaker(models.Model):
    """Book speaker model."""

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(PolymorphicModel, Base):
    """Product model."""

    name = models.CharField(max_length=120)
    description = models.TextField(max_length=255)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # category = models.ForeignKey(
    #     Category,
    #     on_delete=models.SET(get_deleted_category),
    # )
    bookmarks = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="product_bookmarks"
    )
    product_code = models.CharField(
        max_length=255,
        unique=True,
    )
    image = models.URLField()
    extra = models.JSONField()

    # class Meta:
    #     abstract = True

    def __str__(self):
        if self.is_deleted:
            return f"{self.name} [deleted]"
        return self.name


# class BaseInventory(models.Model):
#     """
#     This is a holder for the quantity of products items in stock.
#     It also keeps track of the period, during which that product is available.
#
#     The class implementing this abstract base class, must add a field named 'quantity'
#     of type IntegerField, DecimalField or FloatField.
#     """
#
#     earliest = models.DateTimeField(
#         default=timezone.datetime.min.replace(tzinfo=timezone.get_current_timezone()),
#         db_index=True,
#     )
#
#     latest = models.DateTimeField(
#         default=timezone.datetime.max.replace(tzinfo=timezone.get_current_timezone()),
# #         db_index=True,
# #     )
#
#     class Meta:
#         abstract = True
