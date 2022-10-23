from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django import forms
from django.db.models import Q
from datetime import datetime
import random

from .models import *

def bibliografia(request):
    lista_bibliografia = Bibliografia.objects.all().filter(existe=1).order_by('-fecha_empezado')

    bibliografia = []
    k=0
    while k<len(lista_bibliografia):
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
        'subrayados_huerfanas': subrayados_huerfanas[0:5],
        'referencias_huerfanas': referencias_huerfanas[0:5],
        'zettlecasten_huerfanas': zettlecasten_huerfanas[0:5],
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

def obtener_etiquetas(request, to_edit):

    todas_etiquetas = Etiqueta.objects.all()
    lista_etiquetas = []

    for etiqueta in todas_etiquetas:
        etiqueta_request = request.POST.get("tag_" + str(etiqueta.id))
        if etiqueta_request=="on":
            to_edit.etiqueta.add(etiqueta)
            # lista_etiquetas.append(etiqueta)
        # print("tag_" + str(etiqueta.id))
        # print(request.POST.get("tag_" + str(etiqueta.id)))

    to_edit.save()
    return to_edit

def editar_extracto(request, id):
    to_edit = Extracto.objects.get(id=id)
    to_edit.extracto = request.POST.get('extracto')

    to_edit.etiqueta.clear()
    to_edit = obtener_etiquetas(request, to_edit)

    nueva_biblio = Bibliografia.objects.get(id=request.POST.get('biblio'))
    to_edit.bibliografia = nueva_biblio

    to_edit.posicion = int(request.POST.get('posicion'))
    if request.POST.get('pensar') == "on":
        to_edit.pensar = True
    else:
        to_edit.pensar = False

    to_edit.huerfano = 0

    to_edit.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def editar_extracto_pagina(request, id):
    to_edit = Extracto.objects.get(id=id)
    to_edit.extracto = request.POST.get('extracto')

    if request.POST.get('pensar') == "on":
        to_edit.pensar = True
    else:
        to_edit.pensar = False
    to_edit.save()

    to_edit = obtener_etiquetas(request, to_edit)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def editar_referencia(request, id):
    to_edit = Referencia.objects.get(id=id)
    to_edit.referencia = request.POST.get('Referencia')

    tipo_nuevo = Tipo.objects.filter(nombre=request.POST.get('tipo'))
    if tipo_nuevo.count()>0:
        to_edit.tipo.clear()
        to_edit.tipo.add(*tipo_nuevo)

    nueva_biblio = Bibliografia.objects.get(id=request.POST.get('biblio'))
    to_edit.bibliografia.add(nueva_biblio)

    # to_edit.comentario = request.POST.get('Comentario')

    # to_edit.huerfano = 0

    to_edit.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def editar_zettelcasten(request, id):
    to_edit = Zettelcasten.objects.get(id=id)
    to_edit.contenido = request.POST.get('contenido')

    to_edit.etiqueta.clear()
    to_edit = obtener_etiquetas(request, to_edit)

    # to_edit.huerfano = 0

    to_edit.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def eliminar_extracto(request, id):
    to_remove = Extracto.objects.get(id=id)
    to_remove.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def eliminar_referencia(request, id):
    to_remove = Referencia.objects.get(id=id)
    to_remove.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def eliminar_zet(request, id):
    to_remove = Zettelcasten.objects.get(id=id)
    to_remove.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

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

        num_autor = int(request.POST.get('num_autor'))
        autor_nombre = request.POST.get('autor')
        if autor_nombre=="nuevo":
            autor_nuevo_nombre = request.POST.get('nuevo_autor')
            autor_object = Autor.objects.create(nombre=autor_nuevo_nombre)
            autor_object.save()
        else:
            autor_object = Autor.objects.get(id=autor_nombre)

        nueva_imagen = request.FILES["imagen_nuevo"]
        url = request.POST.get("url")
        fecha = request.POST.get("fecha_inicio")
        fecha_date = datetime.strptime(fecha, '%Y-%m-%d')

        nuevo_biblio = Bibliografia.objects.create(nombre=nuevo_nombre,url=url,fecha_empezado=fecha_date,imagen=nueva_imagen)
        nuevo_biblio.autor.add(autor_object)
        nuevo_biblio.tipo.add(tipo_object)
        nuevo_biblio.huerfano = 0

        if num_autor>1:
            autor_nombre = request.POST.get('autor2')
            if autor_nombre=="nuevo":
                autor_nuevo_nombre = request.POST.get('nuevo_autor2')
                autor_object = Autor.objects.create(nombre=autor_nuevo_nombre)
                autor_object.save()
            else:
                autor_object = Autor.objects.get(id=autor_nombre)
            nuevo_biblio.autor.add(autor_object)
        if num_autor>2:
            autor_nombre = request.POST.get('autor3')
            if autor_nombre=="nuevo":
                autor_nuevo_nombre = request.POST.get('nuevo_autor3')
                autor_object = Autor.objects.create(nombre=autor_nuevo_nombre)
                autor_object.save()
            else:
                autor_object = Autor.objects.get(id=autor_nombre)
            nuevo_biblio.autor.add(autor_object)

        nuevo_biblio.save()

    return HttpResponseRedirect("/bibliografia")


def nueva_etiqueta(request):
    if request.method == 'POST':
        nuevo_nombre = request.POST.get('nombre')
        num_padres = int(request.POST.get("numero_padres"))
        etiqueta_padre_nombre1 = request.POST.get('etiqueta_padre1')
        extracto_id = request.POST.get("extracto")
        zettel_id = request.POST.get("zettel")

        nueva_etiqueta = Etiqueta.objects.create(nombre=nuevo_nombre)

        if etiqueta_padre_nombre1 != "no":
            etiqueta_padre = Etiqueta.objects.get(id=etiqueta_padre_nombre1)
            nueva_etiqueta.etiqueta_padre.add(etiqueta_padre)

        if num_padres>1:
            etiqueta_padre_nombre2 = request.POST.get('etiqueta_padre2')
            etiqueta_padre = Etiqueta.objects.get(id=etiqueta_padre_nombre2)
            nueva_etiqueta.etiqueta_padre.add(etiqueta_padre)

        if num_padres>2:
            etiqueta_padre_nombre3 = request.POST.get('etiqueta_padre3')
            etiqueta_padre = Etiqueta.objects.get(id=etiqueta_padre_nombre3)
            nueva_etiqueta.etiqueta_padre.add(etiqueta_padre)

        nueva_etiqueta.save()

        if extracto_id is not None:
            extracto = Extracto.objects.get(id=int(extracto_id))
            extracto.etiqueta.add(nueva_etiqueta)
            extracto.save()
        if zettel_id is not None:
            zettel = Zettelcasten.objects.get(id=int(zettel_id))
            zettel.etiqueta.add(nueva_etiqueta)
            zettel.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def mostrar_bibliografia(request, id):
    biblio_obj = Bibliografia.objects.get(id=id)
    extracto_list = Extracto.objects.filter(bibliografia=biblio_obj)
    ref_list = Referencia.objects.filter(bibliografia=biblio_obj)
    tag_list  = Etiqueta.objects.all().filter(~Q(nombre="VACIO"))
    biblio_list = Bibliografia.objects.all().filter(existe=1)
    tipo_list = Tipo.objects.all().filter(existe=1)

    template = loader.get_template('unico_biblio.html')

    context = {
        'biblio_obj':biblio_obj,
        'extracto_list':extracto_list,
        'ref_list':ref_list,
        'tipo_list': tipo_list,
        'tag_list': tag_list,
        'biblio_list': biblio_list,
    }

    return HttpResponse(template.render(context, request))

def mostrar_subrayados(request, page=0, filtro="0"):
    lista_subrayados = Extracto.objects.filter(~Q(extracto="VACIO"))
    tag_list = Etiqueta.objects.filter(~Q(nombre="VACIO"))
    bib_list = Bibliografia.objects.all().filter(existe=1)

    tag_id = 0
    bib_id = 0

    init_item = page*15
    end_item = (page+1)*15

    if filtro != "0":
        # La forma que tienen es tagID_bibID, Añadir boton para resetear filtros
        hay_filtro = 0
        print(filtro)
        filtros_arr = filtro.split("_")
        filtro_tag = filtros_arr[0]
        filtro_bib = filtros_arr[1]

        tag_id = filtro_tag[3:]
        if tag_id!="NO":
            tag_id = int(tag_id)
            tag = Etiqueta.objects.get(id=tag_id)
            lista_subrayados = lista_subrayados.filter(etiqueta=tag)

        bib_id = filtro_bib[3:]
        if bib_id!="NO":
            bib_id = int(bib_id)
            bib = Bibliografia.objects.get(id=bib_id)
            lista_subrayados = lista_subrayados.filter(bibliografia=bib)
    else:
        hay_filtro = 1

    ultima_pagina = True
    if lista_subrayados.count() > 0:
        if end_item > lista_subrayados.count():
            ultima_pagina = False
            lista_subrayados = lista_subrayados[init_item:]
        else:
            ultima_pagina = True
            lista_subrayados = lista_subrayados[init_item:end_item]

    pagina_siguiente = page+1
    pagina_anterior = page-1

    template = loader.get_template('mostrar_subrayados.html')

    context = {
        "lista_subrayados": lista_subrayados,
        "pagina_siguiente": pagina_siguiente,
        "pagina_anterior": pagina_anterior,
        "pagina_actual": page,
        "ultima_pagina": ultima_pagina,
        "hay_filtro": hay_filtro,
        "tag_list": tag_list,
        "bib_list": bib_list,
        "filtro":filtro,
        "tag_filter_id": tag_id,
        "bib_filter_id": bib_id,
    }

    return HttpResponse(template.render(context, request))

def mostrar_referencias(request, page=0, filtro="0"):
    lista_referencias = Referencia.objects.filter(~Q(referencia="VACIO"))
    tipo_list = Tipo.objects.filter(existe=1)
    bib_list = Bibliografia.objects.all().filter(existe=1)

    tipo_id = 0
    bib_id = 0

    init_item = page*15
    end_item = (page+1)*15

    if filtro != "0":
        # La forma que tienen es tagID_bibID, Añadir boton para resetear filtros
        hay_filtro = 0
        filtros_arr = filtro.split("_")
        filtro_tipo = filtros_arr[0]
        filtro_bib = filtros_arr[1]

        tipo_id = filtro_tipo[4:]
        if tipo_id!="NO":
            tipo_id = int(tipo_id)
            tipo = Tipo.objects.get(id=tipo_id)
            lista_referencias = lista_referencias.filter(tipo=tipo)

        bib_id = filtro_bib[3:]
        if bib_id!="NO":
            bib_id = int(bib_id)
            bib = Bibliografia.objects.get(id=bib_id)
            lista_referencias = lista_referencias.filter(bibliografia=bib)
    else:
        hay_filtro = 1

    ultima_pagina = True
    if lista_referencias.count() > 0:
        if end_item > lista_referencias.count():
            ultima_pagina = False
            lista_referencias = lista_referencias[init_item:]
        else:
            ultima_pagina = True
            lista_referencias = lista_referencias[init_item:end_item]

    pagina_siguiente = page+1
    pagina_anterior = page-1

    template = loader.get_template('mostrar_referencias.html')

    context = {
        "lista_referencias": lista_referencias,
        "pagina_siguiente": pagina_siguiente,
        "pagina_anterior": pagina_anterior,
        "pagina_actual": page,
        "ultima_pagina": ultima_pagina,
        "hay_filtro": hay_filtro,
        "tipo_list": tipo_list,
        "bib_list": bib_list,
        "filtro":filtro,
        "tipo_filter_id": tipo_id,
        "bib_filter_id": bib_id,
    }

    return HttpResponse(template.render(context, request))


def mostrar_zettlecasten(request, page=0, filtro="0"):
    lista_zettlecasten = Zettelcasten.objects.filter(~Q(contenido="VACIO"))
    tag_list = Etiqueta.objects.filter(~Q(nombre="VACIO"))
    bib_list = Bibliografia.objects.all().filter(existe=1)

    tag_id = 0
    bib_id = 0

    init_item = page*15
    end_item = (page+1)*15

    if filtro != "0":
        # La forma que tienen es tagID_bibID, Añadir boton para resetear filtros
        hay_filtro = 0
        print(filtro)
        filtros_arr = filtro.split("_")
        filtro_tag = filtros_arr[0]
        filtro_bib = filtros_arr[1]

        tag_id = filtro_tag[3:]
        if tag_id!="NO":
            tag_id = int(tag_id)
            tag = Etiqueta.objects.get(id=tag_id)
            lista_zettlecasten = lista_zettlecasten.filter(etiqueta=tag)

        bib_id = filtro_bib[3:]
        if bib_id!="NO":
            bib_id = int(bib_id)
            bib = Bibliografia.objects.get(id=bib_id)
            lista_zettlecasten = lista_zettlecasten.filter(bibliografia=bib)
    else:
        hay_filtro = 1

    ultima_pagina = True
    if lista_zettlecasten.count() > 0:
        if end_item > lista_zettlecasten.count():
            ultima_pagina = False
            lista_zettlecasten = lista_zettlecasten[init_item:]
        else:
            ultima_pagina = True
            lista_zettlecasten = lista_zettlecasten[init_item:end_item]

    pagina_siguiente = page+1
    pagina_anterior = page-1

    template = loader.get_template('mostrar_zettlecasten.html')

    context = {
        "lista_zettlecasten": lista_zettlecasten,
        "pagina_siguiente": pagina_siguiente,
        "pagina_anterior": pagina_anterior,
        "pagina_actual": page,
        "ultima_pagina": ultima_pagina,
        "hay_filtro": hay_filtro,
        "tag_list": tag_list,
        "bib_list": bib_list,
        "filtro":filtro,
        "tag_filter_id": tag_id,
        "bib_filter_id": bib_id,
    }

    return HttpResponse(template.render(context, request))

def mostrar_zettle_individual(request, id_requested):

    zettle_list = Zettelcasten.objects.filter(id=id_requested)
    # id_to_add = Etiqueta.objects.all().values_list('id', flat=True)
    # tag_list = Etiqueta.objects.filter(id__in=id_to_add)
    not_to_add = zettle_list[0].etiqueta.all().values_list('id', flat=True)
    tag_list = Etiqueta.objects.filter(~Q(id__in=not_to_add)).filter(~Q(nombre="VACIO"))

    if zettle_list.count() == 0:
        return HttpResponseRedirect("/zettlecasten")

    zettle_requested = zettle_list[0]
    template = loader.get_template('mostrar_zettle_ind.html')

    zettle_list = Zettelcasten.objects.filter(zettlecasten=zettle_requested)

    context = {
        "zettle_requested": zettle_requested,
        "zettle_list": zettle_list,
        "tag_list": tag_list,
    }

    return HttpResponse(template.render(context, request))

def mostrar_extracto(request, id_requested):
    extracto_list = Extracto.objects.filter(id=id_requested)
    if extracto_list.count() ==0:
        return HttpResponseRedirect("/subrayados")
    else:
        tag_list = Etiqueta.objects.filter(~Q(nombre="VACIO"))
        not_to_add = extracto_list[0].etiqueta.all().values_list('id', flat=True)
        new_tag_list = tag_list.filter(~Q(id__in=not_to_add))
        bib_list = Bibliografia.objects.all().filter(existe=1)
        zettle_list = Zettelcasten.objects.filter(extracto__in=extracto_list)
        context = {
            "extracto": extracto_list[0],
            "bib_list": bib_list,
            "tag_list": tag_list,
            "new_tag_list": new_tag_list,
            "zettle_list": zettle_list,
        }

        template = loader.get_template('mostrar_extracto.html')
        return HttpResponse(template.render(context, request))

# def all_tags_page(request):
#     lista_etiquetas = Etiqueta.objects.filter(~Q(nombre="VACIO"))
#
#     etiquetas_añadidas = []
#     arbol_etiquetas = []
#     etiquetas_padre = []
#
#     for etiqueta in lista_etiquetas:
#         if etiqueta not in etiquetas_añadidas:
#             etiquetas_padre.append(etiqueta)
#             etiquetas_añadidas.append(etiqueta)
#             etiquetas_hijo = etiqueta.etiqueta_set.all()
#             subset_etiquetas = []
#             for sub_etiqueta in etiquetas_hijo:
#                 if etiqueta not in etiquetas_añadidas:
#                     subset_etiquetas.append(sub_etiqueta)
#                     etiquetas_añadidas.append(etiqueta)
#
#     template = loader.get_template('arbol_etiquetas.html')
#
#     context = {
#
#     }

def generar_aleatorio(request):
    zettle_aleatorio = Zettelcasten.objects.filter(en_aleatorio=True)
    extracto_aleatorio = Extracto.objects.filter(en_aleatorio=True)

    zettle_no_aleatorio = Zettelcasten.objects.filter(en_aleatorio=False)
    zettle_no_aleatorio = zettle_no_aleatorio.filter(~Q(contenido="VACIO"))
    extracto_no_aleatorio = Extracto.objects.filter(pensar=True)
    extracto_no_aleatorio = extracto_no_aleatorio.filter(~Q(extracto="VACIO"))
    extracto_no_aleatorio = extracto_no_aleatorio.filter(en_aleatorio=False)

    size_zettel = zettle_no_aleatorio.count()
    size_extracto = extracto_no_aleatorio.count()

    zettle_to_aleat = random.sample(range(0,size_zettel),2)
    extracto_to_aleat = random.sample(range(0,size_extracto),2)

    for zettle in zettle_aleatorio:
        zettle.en_aleatorio = False
        zettle.save()

    for extracto in extracto_aleatorio:
        extracto.en_aleatorio = False
        extracto.save()

    for i in zettle_to_aleat:
        zet_to_mod = zettle_no_aleatorio[i]
        zet_to_mod.en_aleatorio = True
        zet_to_mod.save()

    for i in extracto_to_aleat:
        ext_to_mod = extracto_no_aleatorio[i]
        ext_to_mod.en_aleatorio = True
        ext_to_mod.save()

    return HttpResponseRedirect("/aleatorio")

def mostrar_aleatorios(request):
    zettle_aleatorio = Zettelcasten.objects.filter(en_aleatorio=True)
    extracto_aleatorio = Extracto.objects.filter(en_aleatorio=True)

    template = loader.get_template('mostrar_aleatorio.html')

    context = {
        "zettel_aleatorio": zettle_aleatorio,
        "extracto_aleatorio": extracto_aleatorio,
    }


    return HttpResponse(template.render(context, request))


def crear_zettle_zet(request, id_related):
    tag_list = Etiqueta.objects.filter(~Q(nombre="VACIO"))

    template = loader.get_template('crear_zettle.html')

    context = {
        "id_related": id_related,
        "is_zettle": True,
        "is_ext": False,
        "tag_list": tag_list,
    }


    return HttpResponse(template.render(context, request))


def crear_zettle_ext(request, id_related):
    tag_list = Etiqueta.objects.filter(~Q(nombre="VACIO"))

    template = loader.get_template('crear_zettle.html')

    context = {
        "id_related": id_related,
        "is_zettle": False,
        "is_ext": True,
        "tag_list": tag_list,
    }

    return HttpResponse(template.render(context, request))

def guardar_zet_rel(request):
    if request.method == 'POST':
        is_ext = request.POST.get('is_ext')
        is_zet = request.POST.get('is_zet')
        id_related = request.POST.get("id_related")

        zettle_contenido = request.POST.get("contenido")
        nuevo_zettel = Zettelcasten.objects.create(contenido=zettle_contenido,date_creation=datetime.now(),huerfano=False)
        nuevo_zettel = obtener_etiquetas(request, nuevo_zettel)

        if is_ext == "on":
            extracto = Extracto.objects.get(id=id_related)
            nuevo_zettel.extracto.add(extracto)
        elif is_zet == "on":
            zettel_related = Zettelcasten.objects.get(id=id_related)
            nuevo_zettel.zettelcasten.add(zettelcasten)
        nuevo_zettel.save()

    return HttpResponseRedirect("/aleatorio")

def relacionar_zettel(request, zet_id):

    template = loader.get_template('rel_zet.html')

    context = {
        "zet_id": zet_id,
    }

    return HttpResponse(template.render(context, request))

def relacionar_zettel_ext(request, zet_id, page=0, filtro="0"):

    template = loader.get_template("relacionar_zettel_lista.html")

    lista_subrayados = Extracto.objects.filter(~Q(extracto="VACIO"))
    lista_subrayados = lista_subrayados.filter(en_aleatorio=False)
    en_aleatorio = Extracto.objects.filter(en_aleatorio=True)
    tag_list = Etiqueta.objects.filter(~Q(nombre="VACIO"))
    bib_list = Bibliografia.objects.all().filter(existe=1).order_by("fecha_empezado")

    tag_id = 0
    bib_id = 0

    init_item = page*15
    end_item = (page+1)*15

    if filtro != "0":
        # La forma que tienen es tagID_bibID, Añadir boton para resetear filtros
        hay_filtro = 0
        print(filtro)
        filtros_arr = filtro.split("_")
        filtro_tag = filtros_arr[0]
        filtro_bib = filtros_arr[1]

        tag_id = filtro_tag[3:]
        if tag_id!="NO":
            tag_id = int(tag_id)
            tag = Etiqueta.objects.get(id=tag_id)
            lista_subrayados = lista_subrayados.filter(etiqueta=tag)

        bib_id = filtro_bib[3:]
        if bib_id!="NO":
            bib_id = int(bib_id)
            bib = Bibliografia.objects.get(id=bib_id)
            lista_subrayados = lista_subrayados.filter(bibliografia=bib)
    else:
        hay_filtro = 1

    ultima_pagina = True
    if lista_subrayados.count() > 0:
        if end_item > lista_subrayados.count():
            ultima_pagina = False
            lista_subrayados = lista_subrayados[init_item:]
        else:
            ultima_pagina = True
            lista_subrayados = lista_subrayados[init_item:end_item]

    pagina_siguiente = page+1
    pagina_anterior = page-1

    context = {
        "lista": lista_subrayados,
        "pagina_siguiente": pagina_siguiente,
        "pagina_anterior": pagina_anterior,
        "pagina_actual": page,
        "ultima_pagina": ultima_pagina,
        "hay_filtro": hay_filtro,
        "tag_list": tag_list,
        "bib_list": bib_list,
        "filtro":filtro,
        "tag_filter_id": tag_id,
        "bib_filter_id": bib_id,
        "en_aleatorio": en_aleatorio,
        "rel_with":"relacionar_zettel_ext",
        "is_Ext": True,
        "zet_id":zet_id,
        "prev_page":request.META.get('HTTP_REFERER'),
    }


    return HttpResponse(template.render(context, request))

def relacionar_zettel_zet(request, zet_id, page=0, filtro="0"):

    template = loader.get_template("relacionar_zettel_lista.html")

    lista_zettel = Zettelcasten.objects.filter(~Q(contenido="VACIO"))
    lista_zettel = lista_zettel.filter(en_aleatorio=False)
    en_aleatorio = Zettelcasten.objects.filter(en_aleatorio=True)
    tag_list = Etiqueta.objects.filter(~Q(nombre="VACIO"))

    tag_id = 0

    init_item = page*15
    end_item = (page+1)*15

    if filtro != "0":
        # La forma que tienen es tagID_bibID, Añadir boton para resetear filtros
        hay_filtro = True
        filtro_tag = filtros_arr[0]

        tag_id = filtro_tag[3:]
        if tag_id!="NO":
            tag_id = int(tag_id)
            tag = Etiqueta.objects.get(id=tag_id)
            lista_zettel = lista_zettel.filter(etiqueta=tag)

    else:
        hay_filtro = False

    ultima_pagina = True
    if lista_zettel.count() > 0:
        if end_item > lista_zettel.count():
            ultima_pagina = False
            lista_zettel = lista_zettel[init_item:]
        else:
            ultima_pagina = True
            lista_zettel = lista_zettel[init_item:end_item]

    pagina_siguiente = page+1
    pagina_anterior = page-1

    context = {
        "lista": lista_zettel,
        "pagina_siguiente": pagina_siguiente,
        "pagina_anterior": pagina_anterior,
        "pagina_actual": page,
        "ultima_pagina": ultima_pagina,
        "hay_filtro": hay_filtro,
        "tag_list": tag_list,
        "filtro":filtro,
        "tag_filter_id": tag_id,
        "en_aleatorio": en_aleatorio,
        "rel_with":"relacionar_zettel_zet",
        "is_Ext": False,
        "zet_id":zet_id,
        "prev_page":request.META.get('HTTP_REFERER'),
    }

    return HttpResponse(template.render(context, request))

def rel_zet(request, zet_id, type_rel):
    zet_to_relate = Zettelcasten.objects.get(id=zet_id)
    id_to_add = []

    for key, value in request.POST.items():
        if "item" in key:
            id_to_add.append(int(key.split("_")[1]))

    if type_rel == 1:
        extractos_a_relacionar = Extracto.objects.filter(id__in=id_to_add)
        for item in extractos_a_relacionar:
            zet_to_relate.extracto.add(item)
    elif type_rel == 2:
        zettel_a_relacionar = Zettelcasten.objects.filter(id__in=id_to_add)
        for item in zettel_a_relacionar:
            zet_to_relate.zettlecasten.add(item)

    zet_to_relate.save()
    return HttpResponseRedirect("/zettlecasten_in/"+str(zet_id))


def editar_zet(request, zet_id):

    zet_to_edit = Zettelcasten.objects.get(id=zet_id)
    contenido = request.POST.get("zettlecasten")
    zet_to_edit.contenido = contenido
    zet_to_edit = obtener_etiquetas(request, zet_to_edit)
    zet_to_edit.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def nuevo_extracto(request):

    tag_list  = Etiqueta.objects.all().filter(~Q(nombre="VACIO"))
    biblio_list = Bibliografia.objects.all().filter(existe=1)

    template = loader.get_template('nuevo_extracto.html')
    context = {
        'tag_list':tag_list,
        'biblio_list':biblio_list,
    }

    return HttpResponse(template.render(context, request))

def guardar_nuevo_extracto(request):
    if request.method == 'POST':
        extracto = request.POST.get("extracto")

        biblio_id = int(request.POST.get("biblio"))
        biblio_obj = Bibliografia.objects.get(id=biblio_id)

        posicion = request.POST.get("pos")
        if posicion == "":
            extractos_bib = Extracto.objects.filter(bibliografia=biblio_obj)
            if extractos_bib.count() > 0:
                posicion = extractos_bib[extractos_bib.count()-1].posicion + 1
            else:
                posicion = 1
        else:
            posicion=int(posicion)

        nuevo_extracto = Extracto.objects.create(extracto=extracto, posicion=posicion, bibliografia=biblio_obj)
        nuevo_extracto.save()

        if request.POST.get('pensar') == "on":
            nuevo_extracto.pensar = True
        else:
            nuevo_extracto.pensar = False

        nuevo_extracto.save()

        nuevo_extracto = obtener_etiquetas(request,nuevo_extracto)

    return HttpResponseRedirect("/extracto/"+str(nuevo_extracto.id))

def nuevo_zettel(request):

    tag_list  = Etiqueta.objects.all().filter(~Q(nombre="VACIO"))
    biblio_list = Bibliografia.objects.all().filter(existe=1)

    template = loader.get_template('nuevo_zettel.html')
    context = {
        'tag_list':tag_list,
        'biblio_list':biblio_list,
    }

    return HttpResponse(template.render(context, request))

def guardar_nuevo_zettel(request):
    if request.method == 'POST':
        contenido = request.POST.get("extracto")

        nuevo_zettel = Zettelcasten.objects.create(contenido=contenido)
        nuevo_zettel.save()

        nuevo_zettel = obtener_etiquetas(request,nuevo_zettel)

    return HttpResponseRedirect("/zettlecasten_in/"+str(nuevo_zettel.id))
# Create your views here.
# Create your views here.
