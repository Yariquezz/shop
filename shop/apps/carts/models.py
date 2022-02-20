
from django.db import models
from apps.accounts.models import Customer
from apps.products.models import Products
import uuid


class Cart(models.Model):

    customer = models.ForeignKey(
        Customer,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    public_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )
    is_ordered = models.BooleanField(
        default=False
    )
    updated = models.DateTimeField(
        auto_now=True
    )
    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return "Cart ID: %s" % self.public_id


class CartItems(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        null=True,
        blank=True
    )
    product = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    quantity = models.PositiveIntegerField(default=0)

    @property
    def amount(self):
        return self.product.price * self.quantity

    def __str__(self):
        return 'Product %s cart %s' % (self.product, self.cart)
