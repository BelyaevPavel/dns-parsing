# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-09 09:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_auto_20160809_0828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_reference',
            field=models.URLField(max_length=400),
        ),
    ]
