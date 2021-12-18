from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')
app = Celery('shop')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def send_confirmation_email(self, subject, message):
    while True:
        try:
            send_mail(
                subject,
                message,
                'test_shop@gmail.com',
                [subject],
                fail_silently=False,
            )
            break
        except Exception as err:
            logger.error(err)
