# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-04 13:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20160801_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_sale_city',
            field=models.CharField(default='none', max_length=20),
            preserve_default=False,
        ),
    ]
