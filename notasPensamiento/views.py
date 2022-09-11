from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import *

def index(request):
    lista_bibliografia = Bibliografia.objects.all()

    bibliografia = []
    k=0
    for i in range(0, len(lista_bibliografia)%5):
        linea_libros = []
        for j in range(0,5):
            if k<len(lista_bibliografia):
                linea_libros.append(lista_bibliografia[k])
                k = k+1
        bibliografia.append(linea_libros)

    template = loader.get_template('bibliografia.html')
    context = {
        'bibliografia': bibliografia,
    }

    return HttpResponse(template.render(context, request))
# Create your views here.
