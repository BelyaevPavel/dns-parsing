# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-09 08:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_auto_20160808_0916'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
                ('category_reference', models.CharField(max_length=100)),
                ('check', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='check',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='city',
            field=models.ForeignKey(default=200, on_delete=django.db.models.deletion.CASCADE, to='webapp.Category'),
            preserve_default=False,
        ),
    ]