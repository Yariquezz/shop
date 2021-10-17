from django.db import models
from apps.carts.models import Cart
from django.urls import reverse
import uuid


SHIPMENT_STATUS = (
    ("ORDERED", "Ordered"),
    ("PROCESSED", "Processed"),
    ("SHIPPED", "Shipped"),
    ("RECEIVED", "Received"),
    ("RETTURNED", "Returned"),
    ("DISPUTE", "Dispute"),
)

PAYMENT_STATUS = (
    ("NOT PAID", "Not paid"),
    ("PAID", "Paid"),
    ("RECEIVED", "Received"),
    ("DISPUTE", "Dispute"),
)


class Order(models.Model):
    cart = models.OneToOneField(
        Cart,
        on_delete=models.CASCADE
    )
    shipping_address = models.TextField(
        max_length=500,
        null=True
    )
    payment = models.CharField(
        choices=PAYMENT_STATUS,
        default="NOT_PAID",
        max_length=100
    )
    shipped = models.CharField(
        choices=SHIPMENT_STATUS,
        default="ORDERED",
        max_length=100
    )
    public_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )

    def __str__(self):
        return f"Order ID: {self.public_id}"

    def get_absolute_url(self):
        return reverse(
            'orders:orders_details',
            args=(self.public_id,)
        )
