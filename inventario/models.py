from django.db import models

# Create your models here.

class Categorias(models.Model): 
    id_categoria = models.BigAutoField(primary_key=True)
    categoria = models.CharField('categoria',max_length=50)

class Proveedores(models.Model): 
    id_proveedor = models.BigAutoField(primary_key=True)
    nombre_proveedor = models.CharField('nombre_proveedor',max_length=100)
    telefono_proveedor = models.CharField('telefono_proveedor', max_length=30)
    segundo_telefono = models.CharField('telefono_proveedor', max_length=30, default=None)
    direccion_proveedor = models.CharField('direccion_proveedor', max_length=100)
    observacion = models.CharField('observacion', max_length=500, default=None)