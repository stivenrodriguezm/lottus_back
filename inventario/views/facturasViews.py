from numbers import Number
from rest_framework                                  import views
from rest_framework.response                         import Response
from rest_framework.decorators                       import api_view

from inventario.models import Facturas, Proveedores, Productos, Categorias, Stock
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
    for producto in productos:
        i = 0
        while i < producto['cantidad']:
            product = Productos.objects.only("id_producto").get(id_producto = producto['id_producto'])
            stock = Stock.objects.create(
                id_factura = id_factura,
                id_producto = product,
                valor = producto['valor'],
                disponible = producto['disponible'],
                nota = producto['nota']
            )
            stock.save()
            i += 1
    
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

#STOCK

@api_view(['GET'])
def VerStock(request):
    sql = 'select id_stock as stock, (select nombre_producto from inventario_productos where id_producto = id_producto_id) as producto, (select categoria from inventario_categorias where id_categoria = (select id_categoria_id from inventario_productos where id_producto = id_producto_id)) as categoria, (select id_categoria from inventario_categorias where id_categoria = (select id_categoria_id from inventario_productos where id_producto = id_producto_id)) as categoria, (select nombre_proveedor from inventario_proveedores where id_proveedor = (select id_proveedor_id from inventario_productos where id_producto = id_producto_id)) as proveedor, (select id_factura from inventario_facturas where id_auto = id_factura_id) as factura,valor, disponible, nota from inventario_stock;'
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    
    json = []
    for producto in result:
        json.append({
            'id_stock': producto[0],
            'Producto': producto[1],
            'Categoria_nombre': producto[2],
            'Categoria': producto[3],
            'Proveedor': producto[4],
            'Factura': producto[5],
            'Precio': producto[6],
            'Disponible': producto[7],
            'Nota': producto[8],
        })
    return Response(json)

@api_view(['POST'])
def CrearStock(request, *args, **kwargs):
    data = request.data
    producto = Productos.objects.only("id_producto").get(id_producto = data['id_producto'])
    prod = Productos.objects.filter(id_producto = data['id_producto'])
    categoria = prod[0].categoria
    stock = Stock.objects.create(
        id_producto = producto,
        valor = data['valor'],
        nombre_categoria = categoria,
        disponible = data['disponible'],
        nota = data['nota'],
    )
    id_stock = stock.id_stock
    stock.save()

    stock = Stock.objects.filter(id_stock = id_stock)
    return Response(stock.values())

@api_view(['PUT'])
def EditarStock(request, **kwargs):
    id_stock = kwargs['pk']
    data = request.data
    stock = Stock.objects.get(id_stock = id_stock)
    stock.valor = data['valor']
    stock.disponible = data['disponible']
    stock.nota = data['nota']
    stock.save()

    stock = Stock.objects.filter(id_stock = id_stock)
    print(stock.values())
    return Response(stock.values())


@api_view(['DELETE'])
def EliminarStock(request, **kwargs):
    id_auto = kwargs['pk']
    factura = Stock.objects.get(id_stock = id_auto)
    factura.delete()
    return Response({"El producto en stock fue eliminado"})