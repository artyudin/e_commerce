# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-05 14:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0007_auto_20160905_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='tax_percentage',
            field=models.DecimalField(decimal_places=5, default=0.085, max_digits=20),
        ),
    ]
