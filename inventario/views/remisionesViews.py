from math import prod
from rest_framework                                  import views
from rest_framework.response                         import Response
from rest_framework.decorators                       import api_view

from inventario.models import Remisiones, Stock, Ventas, Transportadores
from django.db import connection
import json

@api_view(['GET'])
def VerRemisiones(request):
    remisiones    = Remisiones.objects.all()
    return Response(remisiones.values())

@api_view(['POST'])
def CrearRemision(request):
    data = request.data

    id_venta = Ventas.objects.only("id_auto").get(id_venta = data["id_venta"])
    id_transportador = Transportadores.objects.only("id_transportador").get(id_transportador = data["id_transportador"])

    transportador = Transportadores.objects.filter(id_transportador = data['id_transportador'])
    transportador = transportador[0]
    transportador = transportador.nombre_transportador

    remision = Remisiones.objects.create(
        id_remision = data["id_remision"],
        id_venta = id_venta,
        id_transportador = id_transportador,
        nombre_transportador = transportador,
        fecha_remision = data["fecha_remision"],
        nota = data["nota"],
    )

    #Definir informacion de los productos a eliminar de stock y guardarlos como string
    productos = data["productos"]
    productos_entregados = []

    for producto in productos:
        sql = f'select id_stock as stock, (select nombre_producto from inventario_productos where id_producto = id_producto_id) as producto, (select categoria from inventario_categorias where id_categoria = (select id_categoria_id from inventario_productos where id_producto = id_producto_id)) as categoria, id_factura_id as venta, valor, disponible, nota from inventario_stock where id_stock = {producto["id_stock"]};'
        cursor = connection.cursor()
        cursor.execute(sql)
        product = cursor.fetchall()
        product = product[0]
        product = f'{product[1]}, {product[2]}, {product[6]}'
        productos_entregados.append({product})
        stock = Stock.objects.only("id_stock").get(id_stock = producto["id_stock"])
        stock.delete()

    remision.productos_entregados = productos_entregados
    remision.save()
    return  Response({"done"})

@api_view(['PUT'])
def EditarRemision(request, **kwargs):
    id_auto = kwargs['pk']
    data = request.data
    remision = Remisiones.objects.only("id_autogenerado").get(id_autogenerado = int(id_auto))
    id_venta = Ventas.objects.only("id_auto").get(id_auto = data["id_venta_id"])
    transportador = Transportadores.objects.only("id_transportador").get(id_transportador = data["id_transportador_id"])

    if(id_venta.id_auto != remision.id_venta_id):
        venta = Ventas.objects.only("id_auto").get(id_auto = data["id_venta_id"])
        remision.id_venta = venta
    
    if(transportador.id_transportador != remision.id_transportador_id):
        id_transportador = Transportadores.objects.only("id_transportador").get(id_transportador = data["id_transportador_id"])
        remision.id_transportador_id = id_transportador
        name = Transportadores.objects.get(id_transportador = id_transportador.id_transportador)
        remision.nombre_transportador = name.nombre_transportador

    remision.id_remision = data['id_remision']
    remision.fecha_remision = data['fecha_remision']
    remision.nota = data['nota']
    remision.save()

    remision = Ventas.objects.filter(id_auto = id_auto)
    return Response(remision.values())

@api_view(['DELETE'])
def EliminarRemision(request, **kwargs):
    id_autogenerado = kwargs['pk']
    remision = Remisiones.objects.get(id_autogenerado = id_autogenerado)
    remision.delete()
    return Response({"La remision fue eliminada"})