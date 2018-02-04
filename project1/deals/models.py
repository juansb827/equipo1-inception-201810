# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #las guaname = models.CharField(max_length=150)
    #lastname = models.CharField(max_length=150)
    img_url = models.CharField(max_length=1000)
    address = models.CharField(max_length=150)
    #email = models.CharField(max_length=150)
    #password = models.CharField(max_length=150)
    city = models.ForeignKey(City, null=True)

class Comment(models.Model):
    #id_comment
    content = models.TextField(max_length=3000)
    email_comment = models.CharField(max_length=150)
    create_date = models.DateTimeField(blank=False)
    user = models.ForeignKey(User, null=False)

#TODO: Agregar modelos faltantes aca






@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
        if(instance.is_staff== False):
            instance.profile.save()


