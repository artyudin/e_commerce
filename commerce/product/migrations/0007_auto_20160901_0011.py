# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-01 00:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_auto_20160901_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to='product/static/product/pics'),
        ),
    ]
