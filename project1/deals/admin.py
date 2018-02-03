# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import City
from .models import Offer
from django.contrib import admin

# Register your models here.
admin.site.register(City)
admin.site.register(Offer)