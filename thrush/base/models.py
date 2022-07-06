"""Base apps models."""
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import Permission
from guardian.shortcuts import assign_perm
import logging

_logger = logging.getLogger(__name__)


class BaseManager(models.Manager):
    """Base model manager."""

    def get_queryset(self):
        """Django built-in method.

        Filter by is_deleted field.
        """
        return super().get_queryset().filter(is_deleted=False)


class AbstractBase(models.Model):
    """Abstract base model implementation."""

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


class BaseComment(Base):
    """Comment model implementation."""

    message = models.CharField(max_length=500)
    reply_to = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, default=""
    )
    is_approved = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ["created_at"]

    def __str__(self):
        if self.is_deleted:
            return f"{self.message} [deleted]"
        return self.message


class BaseStar(models.Model):
    """Star (posts) model implementation."""

    star = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(settings.STAR_MIN_VALUE),
            MaxValueValidator(settings.STAR_MAX_VALUE),
        ]
    )

    class Meta:
        abstract = True
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.star}"


def assign_object_permissions(instance, user=None):
    """Assign permissions per object on groups and users.

    Args:
        instance (Any): Django model instance.
        user (User): user object. Defaults to None.
    """
    for raw_codename in settings.DEFAULT_PERMISSIONS_PER_OBJECT:
        codename = raw_codename.format(model=instance.model_name)
        try:
            permission = Permission.objects.get(codename=codename)
        except Permission.DoesNotExist:
            continue
        for group in permission.group_set.all():
            assign_perm(permission.codename, group, instance)
            _logger.info(
                "Assigned '%s' permission on '%s' group for '%s' object",
                permission.name,
                group.name,
                instance,
            )

        if user:
            user.add_obj_perm(codename, instance)
            _logger.info(
                "Assigned '%s' permission on '%s' user for '%s' object",
                permission.name,
                user.username,
                instance,
            )
