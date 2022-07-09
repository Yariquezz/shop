from django.db import models
from django.urls import reverse
from pytils.translit import slugify
import logging


logger = logging.getLogger(__name__)

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class Blog(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
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
    status = models.IntegerField(
        choices=STATUS,
        default=0
    )
    image = models.ImageField(
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
            url = self.image.url
        except Exception as err:
            logger.error(err)
            url = ''
        return url

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'blog:posts',
            args=(self.slug, )
        )
