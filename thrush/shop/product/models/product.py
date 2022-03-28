"""Product models."""
from datetime import datetime
from django.db import models
# from account.models import User
from base.models import Base
# from polymorphic.models import PolymorphicModel
from django.conf import settings
# from base.models import BaseComment, BaseStar, Category
from base.models import Category
from polymorphic.models import PolymorphicModel


# class Tag(Base):
#     """Tag model implementation."""
#
#     name = models.CharField(max_length=75, unique=True)
#
#     def __str__(self):
#         if self.is_deleted:
#             return f"{self.name} [deleted]"
#         return self.name
#
#
# class Category(Base):
#     """Category model implementation."""
#
#     name = models.CharField(max_length=75)
#     parent = models.ForeignKey(
#         "self",
#         null=True,
#         related_name="category_parent",
#         blank=True,
#         on_delete=models.DO_NOTHING,
#     )
#
#     def __str__(self):
#         if self.is_deleted:
#             return f"{self.name} [deleted]"
#         return self.name
#
#
def get_deleted_category():
    """Retrieve or create a category with DELETED_PRODUCT_CATEGORY_NAME."""
    return Category.objects.get_or_create(name=settings.DELETED_PRODUCT_CATEGORY_NAME)


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
    category = models.ForeignKey(
        Category,
        on_delete=models.SET(get_deleted_category),
    )
    bookmarks = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="product_bookmarks", null=True
    )
    product_code = models.CharField(
        max_length=255,
        unique=True,
    )
    image = models.URLField()
    inventory = models.PositiveIntegerField()
    buy_price = models.PositiveIntegerField()
    sel_price = models.PositiveIntegerField()
    discount = models.PositiveSmallIntegerField(default=0)
    start = models.DateTimeField(default=datetime.utcnow, blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    extra = models.JSONField()
    is_approved = models.BooleanField(default=False)

    # class Meta:
    #     abstract = True

    def __str__(self):
        if self.is_deleted:
            return f"{self.name} [deleted]"
        return self.name
