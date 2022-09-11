from django.db import models

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=150)
    etiqueta_hijo = models.ManyToManyField("self")

class Tipo(models.Model):
    nombre = models.CharField(max_length=150)

class TiposExtracto(models.Model):
    nombre = models.CharField(max_length=150)

class Autor(models.Model):
    nombre = models.CharField(max_length=150)

class Bibliografia(models.Model):
    nombre = models.CharField(max_length=150)
    url = models.CharField(max_length=2048)
    fecha_empezado = models.DateField()
    imagen = models.ImageField()
    autor = models.ManyToManyField(Autor)
    tipo = models.ManyToManyField(Tipo)

class Capitulo(models.Model):
    nombre = models.CharField(max_length=150)
    bibliografia = models.ForeignKey(Bibliografia, on_delete = models.CASCADE)

class Referencia(models.Model):
    referencia = models.CharField(max_length=2048)
    tipo = models.ManyToManyField(Tipo)
    comentario = models.CharField(max_length=1000)
    consultado = models.CharField(max_length=10)
    bibliografia = models.ManyToManyField(Bibliografia)

class Extracto(models.Model):
    extracto = models.CharField(max_length=5000)
    capitulo = models.ForeignKey(Capitulo, on_delete = models.CASCADE)
    tipo = models.ManyToManyField(TiposExtracto)
    posicion = models.IntegerField()
    pensar = models.CharField(max_length=10)
    etiqueta = models.ManyToManyField(Etiqueta)
    bibliografia = models.ForeignKey(Bibliografia, on_delete = models.CASCADE)

class Zettelcasten(models.Model):
    contenido = models.CharField(max_length=5000)
    etiqueta = models.ManyToManyField(Etiqueta)
    extracto = models.ManyToManyField(Extracto)
    zettlecasten = models.ManyToManyField("self")
    date_creation = models.DateField()


# Create your models here.
