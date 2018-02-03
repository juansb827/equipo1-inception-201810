# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class City(models.Model):
    name = models.CharField(max_length=150)
    country = models.CharField(max_length=150)

class Offer(models.Model):
        name = models.CharField(max_length=150)
        img_url = models.CharField(max_length=1000)
        description = models.CharField(max_length=1000)
        start_date = models.DateTimeField(blank=True)
        end_date = models.DateTimeField(blank=True)
        city = models.ForeignKey(City, null=True)
        amount = models.DecimalField(max_digits=10, decimal_places=2)

