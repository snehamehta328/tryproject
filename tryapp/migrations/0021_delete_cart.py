# Generated by Django 3.2 on 2021-06-04 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tryapp', '0020_remove_cart_product_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='cart',
        ),
    ]
