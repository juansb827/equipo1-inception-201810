# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class City(models.Model):
    name = models.CharField(max_length=150)
    country = models.CharField(max_length=150)
