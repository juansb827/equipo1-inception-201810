# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from cloudinary.forms import cl_init_js_callbacks
from django.shortcuts import render

import cloudinary
import cloudinary.uploader
import cloudinary.api

# Create your views here.
from django.urls import reverse

from .models import Offer, Profile
from .forms import UserForm

cloudinary.config(
  cloud_name = os.environ.get('CLOUDINARY_NAME'),
  api_key = os.environ.get('CLOUDINARY_API_KEY'),
  api_secret = os.environ.get('CLOUDINARY_API_SECRET')
)



def index(request):
    lista_promociones=Offer.objects.all()
    context = {'lista_promociones' : lista_promociones}
    return render(request, 'deals/index.html', context)


def add_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            print "Valido", form.is_valid()
            cleaned_data = form.cleaned_data
            username = cleaned_data.get('username')
            print "username", username
            first_name = cleaned_data.get('first_name')
            print "Firstname",cleaned_data.get('first_name')
            last_name = cleaned_data.get('last_name')
            password = cleaned_data.get('password')
            email = cleaned_data.get('email')
            user_model = User()
            user_model.username = username
            user_model.password = password
            user_model.first_name = first_name
            user_model.last_name = last_name
            user_model.email = email
            user_model.save()
            print "address",  cleaned_data.get('address')
            print "city", cleaned_data.get('city')
            print "IMAGEEE", cleaned_data.get('image')
            print "Preferences", list(cleaned_data['preferences'])

            profile = Profile()
            profile.user = user_model
            profile.image = cleaned_data.get('image')
            profile.address = cleaned_data.get('address')
            profile.country = cleaned_data.get('country')
            profile.save()
            profile.preferences = cleaned_data['preferences']
            profile.save();

            return HttpResponseRedirect(reverse('deals:index'))
    else:
        form = UserForm()
        cl_init_js_callbacks(form, request)

    context = {
            'form' : form
       }


    return render(request, 'deals/signup.html', context)


def edit_user(request):
    form = UserForm()
    cl_init_js_callbacks(form, request)

    form
    context = {
        'form': form
    }

    return render(request, 'deals/signup.html', context)

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('deals:index'))