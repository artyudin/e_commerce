# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-01 00:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_auto_20160831_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to='product/pics'),
        ),
    ]