from django.db import models

class Licitacion(models.Model):
    id_licitacion = models.CharField(max_length=50, primary_key=True)
    nombre = models.TextField()
    tipo = models.CharField(max_length=10)
    estado = models.CharField(max_length=100)
    fecha_publicacion = models.DateTimeField()
    descripcion = models.TextField()
    moneda = models.CharField(max_length=10)
    tipo_presupuesto = models.CharField(max_length=100)
    tipo_monto = models.CharField(max_length=100)
    monto = models.CharField(max_length=100)
    organismo = models.TextField()

    def __str__(self):
        return self.nombre