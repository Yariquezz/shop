# Generated by Django 3.2.10 on 2022-01-26 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_products_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='content',
            field=models.JSONField(default={'long': 'dictionary', 'short': 'dict'}, null=True),
        ),
    ]
