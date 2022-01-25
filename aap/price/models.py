"""Price models."""
from datetime import datetime

from django.db import models
from base.models import Base
from base.models import Product


class Price(Base):
    """Price model."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    inventory = models.IntegerField()
    price = models.PositiveIntegerField()
    discount = models.PositiveSmallIntegerField(default=0)
    start = models.DateTimeField(default=datetime.utcnow(), blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        if self.is_deleted:
            return f"{self.product.name} ({self.inventory}:{self.price}/{self.discount}) [deleted]"
        return f"{self.product.name} ({self.inventory}:{self.price}/{self.discount})"

