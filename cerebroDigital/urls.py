"""cerebroDigital URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from notasPensamiento import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),

    # path('.*/(.*.css)$', serve),
    # path('.*/(.*.js)$', serve),
    path('bibliografia', views.bibliografia),
    path('nuevos_items', views.nuevos_items),
    path('procesar_txt', views.procesar_txt),

    path('editar_extracto/<int:id>', views.editar_extracto),
    path('editar_referencia/<int:id>', views.editar_referencia),
    path('eliminar_referencia/<int:id>', views.eliminar_referencia),
    path('eliminar_extracto/<int:id>', views.eliminar_extracto),
    path('extracto_a_ref/<int:id>', views.cambiar_extracto_ref),
    path('editar_zettelcasten/<int:id>', views.editar_zettelcasten),
    path('eliminar_zettel/<int:id>', views.eliminar_zet),

    path('nuevo_biblio', views.nuevo_biblio),
    path('procesar_nuevo_biblio', views.procesar_biblio),
    path('nueva_etiqueta', views.nueva_etiqueta),
    path('bibliografia/<int:id>', views.mostrar_bibliografia),
    path('imprimir_libro/<int:id>', views.imprimir_bibliografia),
    path('imprimir_libro/<int:id>/solopensar/<int:solopensar>', views.imprimir_bibliografia),

    path('subrayados', views.mostrar_subrayados),
    path('subrayados/page/<int:page>', views.mostrar_subrayados),
    path('subrayados/page/<int:page>/filtro/<str:filtro>', views.mostrar_subrayados),
    path('imprimir_lista/page/<int:page>', views.imprimir_lista_subrayados),
    path('imprimir_lista/page/<int:page>/filtro/<str:filtro>', views.imprimir_lista_subrayados),
    path('imprimir_lista/page/<int:page>/solopensar/<int:solopensar>', views.imprimir_lista_subrayados),
    path('imprimir_lista/page/<int:page>/filtro/<str:filtro>/solopensar/<int:solopensar>', views.imprimir_lista_subrayados),
    path('extracto/<int:id_requested>', views.mostrar_extracto),

    path('referencias', views.mostrar_referencias),
    path('referencias/page/<int:page>', views.mostrar_referencias),
    path('referencias/page/<int:page>/filtro/<str:filtro>', views.mostrar_referencias),

    path('zettlecasten', views.mostrar_zettlecasten),
    path('zettlecasten/page/<int:page>', views.mostrar_zettlecasten),
    path('zettlecasten/page/<int:page>/filtro/<str:filtro>', views.mostrar_zettlecasten),
    path('imprimir_zett/page/<int:page>', views.imprimir_zett),
    path('imprimir_zett/page/<int:page>/filtro/<str:filtro>', views.imprimir_zett),
    path('zettlecasten_in/<int:id_requested>', views.mostrar_zettle_individual),

    path('nuevo_zettelcasten_zet/<int:id_related>', views.crear_zettle_zet),
    path('nuevo_zettelcasten_ext/<int:id_related>', views.crear_zettle_ext),
    path('save_new_rel_zet', views.guardar_zet_rel),

    path('aleatorio', views.mostrar_aleatorios),
    path('generar_aleatorio', views.generar_aleatorio),
    path('enviar_aleatorios', views.enviar_aleatorios),

    path('relacionar_zettel/<int:id>', views.relacionar_zettel),
    path('relacionar_zettel_ext/<int:zet_id>', views.relacionar_zettel_ext),
    path('relacionar_zettel_ext/<int:zet_id>/page/<int:page>', views.relacionar_zettel_ext),
    path('relacionar_zettel_ext/<int:zet_id>/page/<int:page>/filtro/<str:filtro>', views.relacionar_zettel_ext),
    path('relacionar_zettel_zet/<int:zet_id>', views.relacionar_zettel_zet),
    path('relacionar_zettel_zet/<int:zet_id>/page/<int:page>', views.relacionar_zettel_zet),
    path('relacionar_zettel_zet/<int:zet_id>/page/<int:page>/filtro/<str:filtro>', views.relacionar_zettel_zet),

    path('relacionar_zettel_ext_form/<int:zet_id>', views.rel_zet, {"type_rel":1}),
    path('relacionar_zettel_zet_form/<int:zet_id>', views.rel_zet, {"type_rel":2}),

    path('editar_zettle/<int:zet_id>', views.editar_zet),

    path('nuevo_extracto',views.nuevo_extracto),
    path('guardar_nuevo_extracto',views.guardar_nuevo_extracto),
    path('nuevo_zettlecasten',views.nuevo_zettel),
    path('guardar_nuevo_zettel',views.guardar_nuevo_zettel),

    path('editar_extracto_pagina/<int:id>', views.editar_extracto_pagina),
    path('process_zettelcasten', views.process_zettelcasten),
    path('', views.bibliografia),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
