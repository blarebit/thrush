"""Payment models."""
from django.db import models
from django.core.validators import MinValueValidator
from polymorphic.models import PolymorphicModel
from account.models import User
from base.models import Base
from account.models import Address
from shop.product.models import Product


class Order(Base):
    """Order model."""

    user = models.ForeignKey(User, related_name="order_user", on_delete=models.DO_NOTHING)
    delivery_address = models.ForeignKey(Address, related_name="order_delivery_address", on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, related_name="order_product", on_delete=models.DO_NOTHING)
    # payment = models.ForeignKey(Payment, related_name="order_payment", on_delete=models.DO_NOTHING, null=True)
    # content = models.TextField()
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )
    total_price = models.PositiveIntegerField()
    invoice_number = models.PositiveIntegerField(null=True)

    # def __str__(self):
    #     if self.is_deleted:
    #         return f"{self.name} [deleted]"
    #     return self.name


class Payment(Base):
    """Payment model."""

    user = models.ForeignKey(User, related_name="payment_user_product", on_delete=models.DO_NOTHING)
    # order = models.On(Order, related_name="order_payment", on_delete=models.DO_NOTHING)
    payment_type = models.CharField(max_length=30)
    # content = models.TextField()
    status = models.CharField(max_length=15, null=True) #, choices=(("success", "success"), ("fail", "fail"), ("cancel", "cancel")))
    bank_response = models.JSONField(null=True)
    total_payment = models.PositiveIntegerField()
    bank_id = models.PositiveIntegerField(null=True)
    batch_number = models.CharField(max_length=45, null=True)
    # invoice_number = models.PositiveIntegerField(null=True)

    # def __str__(self):
    #     if self.is_deleted:
    #         return f"{self.name} [deleted]"
    #     return self.name
