from django.db import models

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=150)
    etiqueta_hijo = models.ManyToManyField("self", blank=True)
    etiqueta_padre = models.ManyToManyField("self", blank=True)

class Tipo(models.Model):
    nombre = models.CharField(max_length=150)
    existe = models.IntegerField(default=1)

class TiposExtracto(models.Model):
    nombre = models.CharField(max_length=150)

class Autor(models.Model):
    nombre = models.CharField(max_length=150)

class Bibliografia(models.Model):
    nombre = models.CharField(max_length=150)
    url = models.CharField(max_length=2048, blank=True, null=True)
    fecha_empezado = models.DateField(blank=True, null=True)
    imagen = models.ImageField(blank=True, null=True)
    autor = models.ManyToManyField(Autor, blank=True, null=True)
    tipo = models.ManyToManyField(Tipo, blank=True, null=True)
    existe = models.IntegerField(default=1)

class Capitulo(models.Model):
    nombre = models.CharField(max_length=150)
    bibliografia = models.ForeignKey(Bibliografia, on_delete = models.CASCADE)

class Referencia(models.Model):
    referencia = models.CharField(max_length=2048)
    tipo = models.ManyToManyField(Tipo)
    comentario = models.CharField(max_length=1000, blank=True)
    consultado = models.CharField(max_length=10, blank=True)
    bibliografia = models.ManyToManyField(Bibliografia)
    en_bibliografia = models.BooleanField(blank=True, null=True) #Mostrar solo las que esten con este falso
    huerfano = models.IntegerField(default=1)

class Extracto(models.Model):
    extracto = models.CharField(max_length=5000, null=True)
    capitulo = models.ForeignKey(Capitulo, on_delete = models.CASCADE, blank=True, null=True)
    tipo = models.ManyToManyField(TiposExtracto, blank=True, null=True)
    posicion = models.IntegerField(blank=True, null=True)
    pensar = models.IntegerField(blank=True, null=True)
    etiqueta = models.ManyToManyField(Etiqueta, null=True)
    bibliografia = models.ForeignKey(Bibliografia, on_delete = models.CASCADE, blank=True, null=True)
    huerfano = models.IntegerField(default=1)
    comentario = models.CharField(max_length=5000, default="", null=True)
    en_aleatorio = models.BooleanField(default=False)

class Zettelcasten(models.Model):
    contenido = models.CharField(max_length=5000)
    etiqueta = models.ManyToManyField(Etiqueta, blank=True, null=True)
    extracto = models.ManyToManyField(Extracto, blank=True, null=True)
    zettlecasten = models.ManyToManyField("self", blank=True, null=True)
    date_creation = models.DateField(blank=True, null=True)
    huerfano = models.IntegerField(default=1, null=True)
    en_aleatorio = models.BooleanField(default=False)


# Create your models here.
