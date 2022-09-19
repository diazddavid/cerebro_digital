from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django import forms
from django.db.models import Q
from datetime import datetime

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

        try:
            if request.POST["contains_biblio"] == "on":
                bibliografia_default = Bibliografia.objects.get(id=request.POST["biblio"])
        except:
            bibliografia_default = Bibliografia.objects.all().filter(existe=0)[0]
        etiqueta_default = Etiqueta.objects.all().filter(id=1)[0]

        if request.POST.get('is_txt') == "on":
            my_file = request.FILES["fichero_txt"]
            is_txt = 1
            highlight_text = "highlight"
            blue_text = "Blue"
            yellow_text = "Yellow"
            pink_text = "Pink"
            orange_text = "Orange"
        elif request.POST.get('is_html') == "on":
            my_file = request.FILES["fichero_html"]
            is_html = 1
            highlight_text = "Subrayado"
            blue_text = "azul"
            yellow_text = "amarillo"
            pink_text = "rosa"
            orange_text = "naranja"

        save_next_line = 0
        pensar = 0
        referencia = 0

        for undecoded_line in my_file:
            line = undecoded_line.decode(encoding="utf8")
            if highlight_text in line:
                save_next_line = 1
                if is_txt:
                    separate_pipe = line.split("|")
                    color_highlight = separate_pipe[0].split(" ")[0]
                elif is_html:
                    separate_pipe = line.split("(")
                    color_highlight = separate_pipe[1].split("-")[0][:-2]

                if color_highlight == blue_text:
                    pensar = 1
                elif color_highlight == yellow_text:
                    pensar = 0
                elif color_highlight == pink_text:
                    referencia = 1
                elif color_highlight == orange_text:
                    type_highlight = 3 #Chapter

                if is_txt:
                    position_txt = separate_pipe[1].split(":")[-1]
                elif is_html:
                    position_txt = separate_pipe[1].split("-")[-1].split(" ")[-1]
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
    to_edit = Extracto.objects.get(id=id)
    to_edit.extracto = request.POST.get('extracto')

    etiqueta_nueva = Etiqueta.objects.filter(nombre=request.POST.get('etiqueta'))
    print(etiqueta_nueva.count())
    if etiqueta_nueva.count()>0:
        to_edit.etiqueta.clear()
        to_edit.etiqueta.add(etiqueta_nueva)

    nueva_biblio = Bibliografia.objects.get(id=request.POST.get('biblio'))
    to_edit.bibliografia = nueva_biblio

    to_edit.posicion = int(request.POST.get('posicion'))
    if request.POST.get('pensar') == "on":
        to_edit.pensar = True
    else:
        to_edit.pensar = False

    to_edit.huerfano = 0

    to_edit.save()
    return HttpResponseRedirect("/nuevos_items")


def eliminar_extracto(request, id):
    to_remove = Extracto.objects.get(id=id)
    to_remove.delete()
    return HttpResponseRedirect("/nuevos_items")


def eliminar_referencia(request, id):
    to_remove = Referencia.objects.get(id=id)
    to_remove.delete()
    return HttpResponseRedirect("/nuevos_items")

def nuevo_biblio(request):
        tag_list  = Etiqueta.objects.all().filter(~Q(nombre="VACIO"))
        biblio_list = Bibliografia.objects.all().filter(existe=1)
        tipo_list = Tipo.objects.all().filter(existe=1)
        autor_list = Autor.objects.all()

        template = loader.get_template('nuevo_biblio.html')
        context = {
            'tag_list':tag_list,
            'biblio_list':biblio_list,
            'tipo_list':tipo_list,
            'autor_list':autor_list,
            'fecha_hoy':datetime.now().strftime("%Y-%m-%d"),
        }

        return HttpResponse(template.render(context, request))

def procesar_biblio(request):
    if request.method == 'POST':
        nuevo_nombre = request.POST.get('Nombre')
        tipo = request.POST.get('tipo')
        tipo_object = Tipo.objects.get(id=tipo)
        autor_nombre = request.POST.get('autor')
        if autor_nombre=="nuevo":
            autor_nuevo_nombre = request.POST.get('nuevo_autor')
            autor_object = Autor.objects.create(nombre=autor_nuevo_nombre)
            autor_object.save()
        else:
            autor_object = Autor.objects.get(id=id)
        nueva_imagen = request.FILES["imagen_nuevo"]
        url = request.POST.get("url")
        fecha = request.POST.get("fecha_inicio")
        fecha_date = datetime.strptime(fecha, '%Y-%m-%d')

        nuevo_biblio = Bibliografia.objects.create(nombre=nuevo_nombre,url=url,fecha_empezado=fecha_date,imagen=nueva_imagen)
        nuevo_biblio.autor.add(autor_object)
        nuevo_biblio.tipo.add(tipo_object)
        nuevo_biblio.save()

    return HttpResponseRedirect("/bibliografia")


# Create your views here.
