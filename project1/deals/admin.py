# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import City
from .models import Offer
from .models import Profile
from .models import Comment
from .models import Category
from django.contrib import admin

# Register your models here.
admin.site.register(City)
admin.site.register(Offer)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Category)
