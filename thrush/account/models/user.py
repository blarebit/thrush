"""Account models."""
import random
import logging

from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group
from django.core.cache import cache
from django.db import models
from base.models import assign_object_permissions
from django.db.models import signals
from django.dispatch import receiver
from guardian.mixins import GuardianUserMixin
from account.verification import send_verification_code
from guardian.models import UserObjectPermissionBase
from guardian.models import GroupObjectPermissionBase
from django.dispatch import receiver
from django.db.models.signals import post_save

_logger = logging.getLogger(__name__)


class User(AbstractUser, GuardianUserMixin):
    """Customized version of Django's User model."""

    model_name = "user"

    is_active = models.BooleanField(default=False)
    mobile = models.CharField(max_length=settings.MOBILE_LENGTH, unique=True)
    mobile_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    image = models.URLField()

    REQUIRED_FIELDS = ["mobile", "password"]

    def __str__(self):
        if self.get_full_name():
            return self.get_full_name()
        return self.username


class UserUserObjectPermission(UserObjectPermissionBase):
    """Guardian user object class."""

    content_object = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_user_content_object"
    )


class UserGroupObjectPermission(GroupObjectPermissionBase):
    """Guardian group object class."""

    content_object = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_group_content_object"
    )


@receiver(post_save, sender=User)
def add_permissions(sender, instance, created, **kwargs):
    if created:
        assign_object_permissions(instance, instance)


@receiver(signals.post_save, sender=User)
def user_default_groups(instance, created, **_):
    """Add a new user in default group."""
    if (
        created
        and not instance.groups.filter(name=settings.DEFAULT_USER_GROUP).exists()
    ):
        try:
            group = Group.objects.get(name=settings.DEFAULT_USER_GROUP)
        except Group.DoesNotExist:
            _logger.error("Default group %s not found!", settings.DEFAULT_USER_GROUP)
            return
        instance.groups.add(group.id)
        instance.save()


@receiver(signals.post_save, sender=User)
def user_verification_code(instance, created, **_):
    """Add a new user in default group."""
    if created:
        verification_code = str(
            random.randint(*settings.VERIFICATION_CODE_LENGTH_RANGE)
        )
        encrypted_verification_code = settings.CRYPTOGRAPHY.encrypt(
            verification_code.encode()
        )
        cache.set(
            encrypted_verification_code,
            instance.id,
            settings.VERIFICATION_CODE_LIFE_TIME,
        )
        send_verification_code(instance, verification_code, encrypted_verification_code)
        _logger.info(
            "call send_verification_code for user: %s[%s], verification code: %s",
            instance.username,
            instance.mobile,
            verification_code,
        )
