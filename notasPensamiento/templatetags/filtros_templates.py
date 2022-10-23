from django import template
register = template.Library()

from notasPensamiento.models import *


@register.filter
def tag_en_subrayado(etiqueta, subrayado):
    for etiqueta_sub in subrayado.etiqueta.all():
        if etiqueta.id == etiqueta_sub.id:
            return True

    return False
