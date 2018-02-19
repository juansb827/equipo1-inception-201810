# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import datetime

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

from .models import Offer, Profile, Category, Comment
from .forms import UserForm, EditUserForm, LoginForm



cloudinary.config(
  cloud_name = os.environ.get('CLOUDINARY_NAME'),
  api_key = os.environ.get('CLOUDINARY_API_KEY'),
  api_secret = os.environ.get('CLOUDINARY_API_SECRET')
)



def index(request):
    mensaje_resultados_vacios = ""
    lista_categorias = Category.objects.all()

    if request.method == "POST":
        nombrePromocion = request.POST.get('nombrePromocion')
        idCategoria = int(request.POST.get('idCategoria'))

        # Si idCategoria es -1, el usuario selecciono "Todas las categorias"
        print "idCategoria = ",idCategoria
        print "nombrePromocion = ", nombrePromocion

        lista_promociones = buscar_promociones(nombrePromocion, idCategoria)

        if lista_promociones != None and lista_promociones.count() > 0:
            mensaje_resultados_vacios = ''
        else:
            mensaje_resultados_vacios ='La consulta no arrojó resultados'
    else:
        lista_promociones = Offer.objects.all()

    print "lista_promociones = ", lista_promociones
    print "lista_categorias = ", lista_categorias
    print "mensaje_resultados_vacios = ", mensaje_resultados_vacios
    #for promocion in lista_promociones:
    #    print "promocion.id = ", promocion.id, " - promocion.name = ", promocion.name, " - promocion.category = ", promocion.category, " - city = ", promocion.city," - start_date",promocion.start_date

    comments = Comment.objects.all()
    context = {'lista_promociones': lista_promociones, 'lista_categorias': lista_categorias, 'comments': comments, 'empty_results_message': mensaje_resultados_vacios}

    return render(request, 'deals/index.html', context)

def buscar_promociones(nombrePromocion, idCategoria):
    lista_promociones = Offer.objects.all()

    if nombrePromocion != "" and idCategoria !=-1:
        lista_promociones = buscar_por_nombre_y_categorias(nombrePromocion, idCategoria)
    elif nombrePromocion != "" and idCategoria ==-1:
        lista_promociones = buscar_por_nombre(nombrePromocion)
    elif nombrePromocion == "" and idCategoria !=-1:
        lista_promociones = buscar_por_categorias(idCategoria)
    return lista_promociones

def buscar_por_nombre_y_categorias(nombrePromocion, idCategoria):
    print "buscar_por_nombre_y_categorias"
    lista_promociones = Offer.objects.all()
    # Si idCategoria es -1, el usuario selecciono "Todas las categorias"
    print "idCategoria = ", idCategoria
    if idCategoria != -1:
        categoria = Category.objects.filter(id=idCategoria)
        print "categoria = ", categoria
        if categoria != None and categoria.count() > 0:
            lista_promociones = Offer.objects.filter(category=categoria).filter(name__icontains=nombrePromocion)

    return lista_promociones

def buscar_por_nombre(nombrePromocion):
    print "buscar_por_nombre"
    lista_promociones = Offer.objects.filter(name__icontains=nombrePromocion)
    return lista_promociones

def buscar_por_categorias(idCategoria):
    print "buscar_por_categorias"
    lista_promociones = Offer.objects.all()
    # Si idCategoria es -1, el usuario selecciono "Todas las categorias"
    print "idCategoria = ", idCategoria
    if idCategoria != -1:
        categoria = Category.objects.filter(id=idCategoria)
        print "categoria = ", categoria
        if categoria != None and categoria.count() > 0:
            lista_promociones = Offer.objects.filter(category=categoria)

    return lista_promociones


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
            user_model.set_password(password)
            user_model.first_name = first_name
            user_model.last_name = last_name
            user_model.email = email
            user_model.save()

            profile = Profile()
            profile.user = user_model
            profile.image = cleaned_data.get('image')
            profile.address = cleaned_data.get('address')
            profile.country = cleaned_data.get('country')
            profile.city = cleaned_data.get('city')
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
    context = {

    }

    if request.method == "POST":
        form = EditUserForm(request.POST)
        context["form"] = form
        form.user = request.user
        print "valido",form.is_valid()
        cambio_password=False
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user_model = request.user
            user_model.username = cleaned_data['username']
            new_password = cleaned_data['password2']
            if new_password:
                user_model.set_password(new_password)
                cambio_password=True

            user_model.first_name = cleaned_data['first_name']
            user_model.last_name = cleaned_data['last_name']
            user_model.email = cleaned_data['email']

            profile = Profile.objects.filter(user=request.user)[0]
            new_image=cleaned_data.get('image');
            print "new Image", new_image
            if new_image :
                profile.image = new_image
            profile.address = cleaned_data.get('address')
            profile.country = cleaned_data.get('country')
            profile.preferences = cleaned_data['preferences']
            user_model.save();
            profile.save();

            if cambio_password:
                return HttpResponseRedirect(reverse('deals:login'))
            else :
                return HttpResponseRedirect(reverse('deals:index'))



    else:
        user = request.user
        print "User", user.id

        profile=Profile.objects.filter(user=user)[0]
        form = EditUserForm(initial={
            'user' : user,
            'profile' : profile,
            'username': user.username,
            'first_name' : user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'country' : profile.country,
            'city' : profile.city,
            'address' : profile.address,
            'image' : profile.image,
            'preferences' : profile.preferences.all().values_list('pk', flat=True)


        })

        print "img",profile.image
        context["user_img"] = profile.image
        context["form"] = form

        cl_init_js_callbacks(form, request)
    context["edit"] = True
    return render(request, 'deals/signup.html', context)


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('deals:index'))

def login_user(request):
    form = LoginForm()
    cl_init_js_callbacks(form, request)
    form
    context = {
        'form': form
    }

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            username = cleaned_data.get('username')
            password = cleaned_data.get('password')

            user_exists = User.objects.filter(username=username)
            print "username = ", username, " password = ", password
            print "user_exists = ", user_exists
            if user_exists != None and user_exists.count()>0:
                profile_exists = Profile.objects.filter(user=user_exists)
                print "profile_exists = ", profile_exists
                if profile_exists != None and profile_exists.count()>0:
                    login(request, user_exists.first())
                    return HttpResponseRedirect(reverse('deals:index'))
            else:
                context['login_message'] = 'Login fallido'
                return render(request, 'deals/login.html', context )
    else:
        return render(request, 'deals/login.html', context)

def add_comment(request):
    if request.method == 'POST':
            content = request.POST.get('comentario')
            email = request.POST.get('email')
            date = datetime.datetime.now()
            user = request.user
            offer_id = request.POST.get('oferta')
            comment = Comment.objects.create(
                content=content,
                email_comment=email,
                create_date=date,
                user=user,
                offer_id=offer_id)
            comment.save()
    return HttpResponseRedirect(reverse('deals:index'))
