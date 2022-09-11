from django.contrib import admin

from notasPensamiento.models import *

@admin.register(Bibliografia)
class BibliografiaAdmin(admin.ModelAdmin):
    pass

@admin.register(Referencia)
class ReferenciaAdmin(admin.ModelAdmin):
    pass

@admin.register(Extracto)
class ExtractoAdmin(admin.ModelAdmin):
    pass

@admin.register(Zettelcasten)
class ZettelcastenAdmin(admin.ModelAdmin):
    pass

@admin.register(Capitulo)
class CapituloAdmin(admin.ModelAdmin):
    pass

@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    pass

@admin.register(Tipo)
class TipoAdmin(admin.ModelAdmin):
    pass

@admin.register(TiposExtracto)
class TiposExtractoAdmin(admin.ModelAdmin):
    pass

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    pass
