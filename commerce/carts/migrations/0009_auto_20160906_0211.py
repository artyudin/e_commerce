# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-06 02:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0008_cart_tax_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=20),
        ),
    ]
