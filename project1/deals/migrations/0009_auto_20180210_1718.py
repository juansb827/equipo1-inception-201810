# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-10 17:18
from __future__ import unicode_literals

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0008_auto_20180210_0203'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='img_url',
        ),
        migrations.AddField(
            model_name='profile',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='preferences',
            field=models.ManyToManyField(to='deals.Category'),
        ),
    ]
