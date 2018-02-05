# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from .models import Offer


def index(request):
    lista_promociones=Offer.objects.all()
    context = {'lista_promociones' : lista_promociones}
    return render(request,'deals/index.html',context)