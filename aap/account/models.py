"""Account models."""
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models import signals
from django.dispatch import receiver


class Profile(models.Model):
    """User profile model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=11, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)

    class Meta:
        db_table = "auth_profile"
        unique_together = [["user", "mobile"], ["user", "phone"]]

    def __str__(self):
        return self.user.get_full_name()


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
