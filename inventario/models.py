from django.db import models
from django.db.models.deletion import CASCADE

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

class Productos(models.Model): 
    id_producto = models.BigAutoField(primary_key=True)
    id_proveedor = models.ForeignKey(Proveedores, CASCADE, default=None)
    id_categoria = models.ForeignKey(Categorias, CASCADE, default=None)
    nombre_proveedor = models.CharField('nombre_proveedor',max_length=255, default=None)
    categoria = models.CharField('categoria',max_length=255, default=None)
    nombre_producto = models.CharField('nombre_producto',max_length=255)
    medidas = models.CharField('medidas',max_length=255,default=None)
    costo = models.BigIntegerField('costo', default=0)
    tiempo_entrega = models.IntegerField('tiempo_entrega', null=True)
    nota = models.CharField('nota',max_length=255, null=True)

class Facturas(models.Model): 
    id_auto = models.BigAutoField(primary_key=True)
    id_proveedor = models.ForeignKey(Proveedores, CASCADE, default=None)
    id_factura = models.IntegerField('id_factura', null=True)
    nombre_proveedor = models.CharField(max_length=100, editable=True, null=True)
    fecha_despacho = models.CharField(max_length=50, editable=True, null=True)
    fecha_pago = models.CharField(max_length=50, editable=True, null=True)
    valor = models.BigIntegerField('valor', default=0, editable=True)
    pagada = models.BooleanField('pagada', null=True)
    nota = models.CharField(max_length=500, editable=True, null=True)