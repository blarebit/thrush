"""Account app models."""
from base.models import Base
from django.db import models
from .user import User


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
