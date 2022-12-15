from numbers import Number
from rest_framework                                  import views
from rest_framework.response                         import Response
from rest_framework.decorators                       import api_view

from inventario.models import Facturas, Proveedores, Productos, Categorias
from django.db import connection
import json

@api_view(['GET'])
def VerFacturas(request):
    categorias    = Facturas.objects.all()
    return Response(categorias.values())

@api_view(['POST'])
def CrearFactura(request, *args, **kwargs):
    data = request.data
    productos = data['productos']

    proveedor = Proveedores.objects.only("id_proveedor").get(id_proveedor = data['id_proveedor'])
    nombre_proveedor = Proveedores.objects.only("nombre_proveedor").get(id_proveedor = data['id_proveedor'])
    nombre_proveedor = nombre_proveedor.nombre_proveedor

    factura = Facturas.objects.create(
        id_factura = data['id_factura'],
        id_proveedor = proveedor,
        nombre_proveedor = nombre_proveedor,
        fecha_despacho = data['fecha_despacho'],
        fecha_pago = data['fecha_pago'],
        pagada = data['pagada'],
        valor = data['valor'],
        nota = data['nota'],
    )
    id_auto = factura.id_auto
    factura.save()
    id_factura = Facturas.objects.only("id_auto").get(id_auto = id_auto)
    # Crear producto en Stock
    # for producto in productos:
    #     i = 0
    #     while i < producto['cantidad']:
    #         product = Productos.objects.only("id_producto").get(id_producto = producto['id_producto'])
    #         stock = Stock.objects.create(
    #             id_factura = id_factura,
    #             id_producto = product,
    #             valor = producto['valor'],
    #             disponible = producto['disponible'],
    #             nota = producto['nota']
    #         )
    #         stock.save()
    #         i += 1
    
    factura = Facturas.objects.filter(id_auto = id_auto)
    return Response(factura.values())

@api_view(['PUT'])
def EditarFactura(request, **kwargs):
    id_auto = kwargs['pk']
    data = request.data

    nombre_proveedor = Proveedores.objects.only("nombre_proveedor").get(id_proveedor = data['id_proveedor_id'])
    nombre_proveedor = nombre_proveedor.nombre_proveedor

    factura = Facturas.objects.get(id_auto = id_auto)

    factura.id_proveedor_id = data['id_proveedor_id']
    factura.id_factura = data['id_factura']
    factura.nombre_proveedor = nombre_proveedor
    factura.fecha_despacho = data['fecha_despacho']
    factura.fecha_pago = data['fecha_pago']
    factura.valor = data['valor']
    factura.pagada = data['pagada']
    factura.nota = data['nota']
    factura.save()

    fact = Facturas.objects.filter(id_auto = id_auto)

    
    return Response(fact.values())

@api_view(['DELETE'])
def EliminarFactura(request, **kwargs):
    id_auto = kwargs['pk']
    factura = Facturas.objects.get(id_auto = id_auto)
    factura.delete()
    return Response({"La factura se ha eliminado."})