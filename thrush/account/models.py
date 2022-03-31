"""Account models."""
import random

from base.models import Base
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.cache import cache
from django.db import models
from django.db.models import signals
from django.dispatch import receiver

from .verification import send_verification_code


class User(AbstractUser):
    """Customized version of Django's User model."""

    is_active = models.BooleanField(default=False)
    mobile = models.CharField(max_length=settings.MOBILE_LENGTH, unique=True)
    mobile_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    image = models.URLField()

    REQUIRED_FIELDS = ["mobile", "password"]

    def __str__(self):
        return self.get_full_name()


@receiver(signals.post_save, sender=User)
def user_default_groups(instance, created, **_):
    """Add a new user in default group."""
    if (
        created
        and not instance.groups.filter(name=settings.DEFAULT_USER_GROUP).exists()
    ):
        group = Group.objects.get(name=settings.DEFAULT_USER_GROUP)
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


class Address(Base):
    """Address model"""

    user = models.ForeignKey(
        User, related_name="address_user", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100, null=False, default="home")
    country = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=150, null=False)
    state = models.CharField(max_length=150, null=False)
    post_code = models.CharField(max_length=10, null=False)
    address = models.CharField(max_length=255, null=False)
    street = models.CharField(max_length=255, null=True)
    house_number = models.CharField(max_length=5, null=False)
    floor = models.CharField(max_length=3, null=False)
    unit = models.CharField(max_length=3, null=False)
    is_default = models.BooleanField(default=True)

    class Meta:
        unique_together = [("user", "is_default")]

    def __str__(self):
        return f"{self.name} [{self.is_default}]"
