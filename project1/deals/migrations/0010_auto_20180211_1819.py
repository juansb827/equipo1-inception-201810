# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-11 18:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0009_auto_20180210_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
