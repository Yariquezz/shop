from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class DiscountCard(models.Model):
    card_no = models.TextField(max_length=500, null=True)
    benefits = models.JSONField(
        null=True,
    )

    def __str__(self):
        return "Card: %s" % self.card_no


class Customer(models.Model):
    user = models.OneToOneField(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    phone = models.CharField(
        max_length=20,
        null=True
    )
    address = models.TextField(
        max_length=500,
        null=True
    )
    discount_card = models.ForeignKey(
        DiscountCard,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        if self.user:
            name = self.user.username
        else:
            name = 'Anonymous'

        return name

    @ receiver(post_save, sender=User)
    def create_customer(sender, instance, created, **kwargs):
        if created:
            Customer.objects.create(user=instance)

    @ receiver(post_save, sender=User)
    def save_customer(sender, instance, **kwargs):
        instance.customer.save()
