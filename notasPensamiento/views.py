from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django import forms
from django.db.models import Q

from .models import *

def bibliografia(request):
    lista_bibliografia = Bibliografia.objects.all().filter(existe=1)

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


def nuevos_items(request):
    subrayados_huerfanas = Extracto.objects.all().filter(~Q(extracto="VACIO")&Q(huerfano=1))
    referencias_huerfanas = Referencia.objects.all().filter(~Q(referencia="VACIO")&Q(huerfano=1))
    zettlecasten_huerfanas = Zettelcasten.objects.all().filter(~Q(contenido="VACIO")&Q(huerfano=1))
    tag_list  = Etiqueta.objects.all().filter(~Q(nombre="VACIO"))
    biblio_list = Bibliografia.objects.all().filter(existe=1)
    tipo_list = Tipo.objects.all().filter(existe=1)

    template = loader.get_template('nuevos_items.html')
    context = {
        'subrayados_huerfanas': subrayados_huerfanas,
        'referencias_huerfanas': referencias_huerfanas,
        'zettlecasten_huerfanas': zettlecasten_huerfanas,
        'tag_list':tag_list,
        'biblio_list':biblio_list,
        'tipo_list':tipo_list,
    }

    return HttpResponse(template.render(context, request))

def procesar_txt(request):
    if request.method == 'POST':

        if request.POST["contains_biblio"] == "on":
            bibliografia_default = Bibliografia.objects.get(id=request.POST["biblio"])
        else:
            bibliografia_default = Bibliografia.objects.all().filter(existe=0)[0]
        etiqueta_default = Etiqueta.objects.all().filter(id=1)[0]
        my_file = request.FILES["fichero_txt"]

        save_next_line = 0
        pensar = 0
        referencia = 0

        for undecoded_line in my_file:
            line = undecoded_line.decode(encoding="utf8")
            if "highlight" in line:
                save_next_line = 1
                separate_pipe = line.split("|")

                color_highlight = separate_pipe[0].split(" ")[0]
                if color_highlight == "Blue":
                    pensar = 1
                elif color_highlight == "Yellow":
                    pensar = 0
                elif color_highlight == "Pink":
                    referencia = 1
                elif color_highlight == "Orange":
                    type_highlight = 3 #Chapter

                position_txt = separate_pipe[1].split(":")[-1]
                posicion = int(position_txt.replace(",",""))
                continue

            if save_next_line==1:
                text = line
                save_next_line = 0
                extracto = line

                if referencia != 1:
                    nuevo_extracto = Extracto.objects.create(extracto=extracto, posicion=posicion, pensar=pensar, bibliografia=bibliografia_default)
                    nuevo_extracto.etiqueta.add(etiqueta_default)
                    nuevo_extracto.save()
                    print("Processed Extracto")
                else:
                    nueva_referencia = Referencia.objects.create(referencia=extracto, huerfano=1)
                    nueva_referencia.bibliografia.add(bibliografia_default)
                    nueva_referencia.save()
                    print("Processed Referencia")

                pensar = 0
                referencia = 0

    return nuevos_items(request)

def editar_extracto(request, id):
    print(id)
    return nuevos_items(request)


def eliminar_extracto(request, id):
    print("entra")
    to_remove = Extracto.objects.get(id=id)
    to_remove.delete()
    return HttpResponseRedirect("/nuevos_items")


def eliminar_referencia(request, id):
    print("entra")
    to_remove = Referencia.objects.get(id=id)
    to_remove.delete()
    return HttpResponseRedirect("/nuevos_items")

# Create your views here.
