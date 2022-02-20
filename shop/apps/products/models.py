from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid
import logging


logger = logging.getLogger(__name__)

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'products:search_results',
            kwargs=dict(Q=self.name),
        )


class Products(models.Model):
    title = models.CharField(
        max_length=200,
        unique=True
    )
    product_code = models.CharField(
        max_length=200,
        unique=True,
        null=True,
        editable=False,
    )
    price = models.FloatField()
    discount = models.FloatField(
        default=0,
        null=True
    )
    rating = models.FloatField(
        default=0,
        blank=0,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(5.0)
        ]
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        editable=False
    )
    updated_on = models.DateTimeField(
        auto_now=True
    )
    created_on = models.DateTimeField(
        auto_now_add=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    description = models.TextField(
        null=True,
    )
    content = models.JSONField(
        null=True,
        default=dict
    )
    status = models.IntegerField(
        choices=STATUS,
        default=0
    )
    image_1 = models.ImageField(
        null=True,
        blank=True
    )
    image_2 = models.ImageField(
        null=True,
        blank=True
    )
    image_3 = models.ImageField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = [
                self.image_1.url,
                self.image_2.url,
                self.image_3.url,
            ]
        except Exception as err:
            logger.error(err)
            url = ''
        return url

    @property
    def discounted(self):
        if self.discount:
            return round(self.price * (1 + self.discount / 100), 10)
        else:
            return self.price

    def save(self, *args, **kwargs):
        self.product_code = str(uuid.uuid4())
        self.slug = slugify(self.title + self.product_code)
        super(Products, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'products:product_detail',
            args=(self.slug, )
        )
