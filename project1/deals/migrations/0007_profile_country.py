# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-10 01:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0006_auto_20180204_2101'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='country',
            field=models.CharField(max_length=30, null=True),
        ),
    ]