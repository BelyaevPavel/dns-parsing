# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-09 15:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0010_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_price',
            field=models.FloatField(default=0),
        ),
    ]
