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

class Vendedores(models.Model):
    id_vendedor = models.BigAutoField(primary_key=True)
    nombre_vendedor = models.CharField('nombre_vendedor', null=True, max_length=100)
    telefono_vendedor = models.CharField('telefono_vendedor', null=True, max_length=25)
    cedula_vendedor = models.CharField('cedula_vendedor', null=True, max_length=25)
    correo_vendedor = models.CharField('correo_vendedor', null=True, max_length=100)
    direccion_vendedor = models.CharField('direccion_vendedor', null=True, max_length=100)
    activo = models.BooleanField('activo', default=True)
    nombre_contacto_emergencia = models.CharField('nombre_contacto_emergencia', null=True, max_length=100)
    numero_contacto_emergencia = models.CharField('numero_contacto_emergencia', null=True, max_length=100)

class Transportadores(models.Model):
    id_transportador = models.BigAutoField(primary_key=True)
    nombre_transportador = models.CharField('nombre_transportador', null=True, max_length=100)
    telefono_transportador = models.CharField('telefono_transportador', null=True, max_length=50)
    cedula_transportador = models.CharField('cedula_transportador', null=True, max_length=50)
    direccion_transportador = models.CharField('direccion_transportador', null=True, max_length=100)
    nombre_contacto_emergencia = models.CharField('nombre_contacto_emergencia', null=True, max_length=100)
    numero_contacto_emergencia = models.CharField('numero_contacto_emergencia', null=True, max_length=100)

class Clientes(models.Model):
    id_cliente = models.BigAutoField(primary_key=True)
    nombre_cliente = models.CharField('cedula_vendedor', null=True, max_length=250)
    cedula_cliente = models.CharField('correo_vendedor', null=True, max_length=250)
    direccion_cliente = models.CharField('direccion_cliente', null=True, max_length=250)
    ciudad_cliente = models.CharField('ciudad_cliente', null=True, max_length=250)
    correo_cliente = models.CharField('correo_cliente', null=True, max_length=250)
    telefono_cliente = models.CharField('telefono_cliente', null=True, max_length=250)
    
class Ventas(models.Model):
    id_auto = models.BigAutoField(primary_key=True)
    id_venta = models.IntegerField('id_venta',null=True)
    id_vendedor = models.ForeignKey(Vendedores, on_delete=models.CASCADE, default=None)
    nombre_vendedor = models.CharField('nombre_vendedor', max_length=150, default=None)
    fecha_venta = models.CharField('telefono_vendedor', null=True, max_length=50)
    nombre_cliente = models.CharField('nombre_cliente', null=True, max_length=150)
    cedula_cliente = models.CharField('cedula_cliente', null=True, max_length=50)
    fecha_entrega = models.CharField('numero_contacto_emergencia', null=True, max_length=50)
    entregado = models.BooleanField('numero_contacto_emergencia', null=True)
    id_cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, default=None)
    valor_venta = models.BigIntegerField('valor_venta', null=True)
    abono = models.BigIntegerField('abono', null=False, default=0)
    saldo = models.BigIntegerField('saldo', null=True)

class Pedidos(models.Model):
    id_auto = models.BigAutoField(primary_key=True)
    id_orden_pedido = models.IntegerField('id_orden_pedido', null=True)
    valor_total = models.BigIntegerField('valor_total', null=True)
    id_venta = models.ForeignKey(Ventas, on_delete=models.CASCADE, default=None)
    id_proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE, default=None)
    id_vendedor = models.ForeignKey(Vendedores, on_delete=models.CASCADE, default=False)
    tela = models.CharField('tela', null=True, max_length=250)
    fecha = models.CharField('fecha', null=True, max_length=250)
    fecha_despacho = models.CharField('fecha_despacho', null=True, max_length=250)
    enviada = models.CharField('fecha_despacho', null=True, max_length=250)
    recibida = models.BooleanField('recibida', null=True)

class Remisiones(models.Model):
    id_autogenerado = models.BigAutoField(primary_key=True)
    id_remision = models.IntegerField('id_remision', null=True)
    id_venta = models.ForeignKey(Ventas, on_delete=models.CASCADE, default=None)
    id_transportador = models.ForeignKey(Transportadores, on_delete=models.CASCADE, default=None)
    nombre_transportador = models.CharField('nombre_transportador', max_length=150, null=True)
    productos_entregados = models.CharField('productos_entregados', max_length=2500, null=True)
    fecha_remision = models.CharField('fecha_remision', max_length=50, null=True)
    nota = models.CharField('nota', max_length=2000, null=True)

class Stock(models.Model):
    id_stock = models.BigAutoField(primary_key=True)
    id_factura = models.ForeignKey(Facturas, on_delete=models.CASCADE, default=None, null=True)
    id_producto = models.ForeignKey(Productos, on_delete=models.CASCADE, default=None)
    nombre_categoria = models.CharField('nombre_categoria', max_length=255,null=True)
    valor = models.BigIntegerField('valor', null=True)
    disponible = models.BooleanField('disponible', null=True)
    nota = models.CharField('nota', max_length=255,null=True)
