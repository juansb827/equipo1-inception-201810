# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class City(models.Model):
    name = models.CharField(max_length=150)
    country = models.CharField(max_length=150)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __unicode__(self):
        return self.name


class Offer(models.Model):
    category = models.ForeignKey(Category, null=True)
    name = models.CharField(max_length=150)
    img_url = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    start_date = models.DateTimeField(blank=True)
    end_date = models.DateTimeField(blank=True)
    city = models.ForeignKey(City, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __unicode__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferences = models.ManyToManyField(Category)
    country = models.CharField(max_length=30,null=True)
    city = models.CharField(max_length=30, null=True)
    image = CloudinaryField('image', null=True)
    address = models.CharField(max_length=150)


    def __unicode__(self):
        return self.user.username + "-" + self.user.email


class Comment(models.Model):
    # id_comment
    content = models.TextField(max_length=3000)
    email_comment = models.CharField(max_length=150)
    create_date = models.DateTimeField(blank=False)
    user = models.ForeignKey(User, null=False)




