# Generated by Django 3.2.10 on 2022-01-26 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='content',
            field=models.JSONField(default={'default': None}, null=True),
        ),
    ]