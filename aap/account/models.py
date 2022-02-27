"""Account models."""
# from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from base.models import Base


class User(AbstractUser):
    """Customized version of Django's User model."""

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        blank=True,
        null=True,
    )
    mobile = models.CharField(max_length=settings.MOBILE_LENGTH)
    mobile_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    image = models.URLField()
    # address = models.ForeignKey(Address, related_name="address_user", on_delete=models.CASCADE, null=True)
    # is_verified = models.BooleanField(default=False)
    # verify_code = models.CharField(max_length=settings.VERIFY_CODE_LENGTH)
    # start_verify = models.DateTimeField(blank=True, null=True),
    # expire_verify = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.get_full_name()


@receiver(signals.post_save, sender=User)
def add_user_in_default_group(instance, created, **_):
    """Add a new user in default group."""
    if (
        created
        and not instance.groups.filter(name=settings.DEFAULT_USER_GROUP).exists()
    ):
        default_group = Group.objects.get_or_create(name=settings.DEFAULT_USER_GROUP)
        instance.groups.add(default_group[0].id)
        instance.save()


# class Address(models.Model):
class Address(Base):
    """Address model"""

    name = models.CharField(max_length=100, null=False, default="home")
    user = models.ForeignKey(User, related_name="address_user", on_delete=models.CASCADE)
    country = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=150, null=False)
    state = models.CharField(max_length=150, null=False)
    post_code = models.CharField(max_length=10, null=False)
    address = models.CharField(max_length=255, null=False)
    street = models.CharField(max_length=255, null=True)
    house_number = models.CharField(max_length=5, null=False)
    floor = models.CharField(max_length=3, null=False)
    unit = models.CharField(max_length=3, null=False)

