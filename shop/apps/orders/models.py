from django.db import models
from apps.carts.models import Cart
from django.urls import reverse
from datetime import datetime

SHIPMENT_STATUS = (
    ("Замовлено", "Ordered"),
    ("Опрацьовано", "Processed"),
    ("В доставці", "Shipped"),
    ("Отримано", "Received"),
    ("Повернено", "Returned"),
    ("В розгляді", "Dispute"),
)

PAYMENT_STATUS = (
    ("Не оплачено", "Not_paid"),
    ("Оплачено", "Paid"),
    ("Повернено", "Received"),
    ("Оскаржено", "Dispute"),
)


def get_order_id():
    return datetime.now().strftime('%Y%m%d%H%M%S')


class Warehouse(models.Model):

    title = models.CharField(
        'Назва',
        max_length=255,
        db_index=True
    )

    address = models.CharField(
        'Адреса',
        max_length=255,
        db_index=True
    )

    @property
    def full_name(self):
        return '{}, {}'.format(self.title, self.address)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Відділення Нової пошти'


class Order(models.Model):
    cart = models.OneToOneField(
        Cart,
        on_delete=models.CASCADE
    )
    shipping_address = models.CharField(
        null=True,
        blank=True,
        max_length=1000
    )
    payment = models.CharField(
        choices=PAYMENT_STATUS,
        default="Не оплачено",
        max_length=100
    )
    shipped = models.CharField(
        choices=SHIPMENT_STATUS,
        default="Замовлено",
        max_length=100
    )
    public_id = models.CharField(
        default=get_order_id,
        editable=False,
        max_length=100
    )

    def __str__(self):
        return "Order ID: %s" % self.public_id

    def get_absolute_url(self):
        return reverse(
            'orders:orders_details',
            args=(self.public_id,)
        )
