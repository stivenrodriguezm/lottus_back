from rest_framework                                  import views
from rest_framework.response                         import Response
from rest_framework.decorators                       import api_view

from inventario.models import Productos, Proveedores, Categorias

@api_view(['GET'])
def VerProductos(request):
    productos    = Productos.objects.all()
    return Response(productos.values())

@api_view(['GET'])
def ProductosPorCategoria(request, *args,**kwargs):
    data = kwargs['categoria']
    id_categoria = Categorias.objects.filter(categoria = data)
    id_categoria = id_categoria[0].id_categoria
    productos    = Productos.objects.filter(id_categoria = 1)
    return Response(productos.values())

@api_view(['POST'])
def CrearProducto(request, *args, **kwargs):
    data = request.data
    proveedor = Proveedores.objects.only("id_proveedor").get(id_proveedor = data['id_proveedor'])
    categoria = Categorias.objects.only("id_categoria").get(id_categoria = data['id_categoria'])
    nombre_proveedor = Proveedores.objects.only("nombre_proveedor").get(id_proveedor = data['id_proveedor'])
    nombre_categoria = Categorias.objects.only("categoria").get(id_categoria = data['id_categoria'])
    producto = Productos.objects.create(
        id_proveedor = proveedor,
        id_categoria = categoria,
        nombre_proveedor = nombre_proveedor.nombre_proveedor,
        categoria = nombre_categoria.categoria,
        nombre_producto = data['nombre_producto'],
        medidas = data['medidas'],
        costo = data['costo'],
        tiempo_entrega = data['tiempo_entrega'],
        nota = data['nota'],
    )

    id_producto = producto.id_producto
    producto.save()
    producto = Productos.objects.filter(id_producto = id_producto)
    return Response(producto.values())

@api_view(['PUT'])
def EditarProducto(request, **kwargs):
    id_producto = kwargs['pk']
    data = request.data
    
    productos = Productos.objects.get(id_producto = id_producto)

    if data['id_proveedor_id']:
        id_proveedor = Proveedores.objects.only("id_proveedor").get(id_proveedor = data['id_proveedor_id'])
        productos.id_proveedor = id_proveedor
        nombre_proveedor = Proveedores.objects.only("nombre_proveedor").get(id_proveedor = data['id_proveedor_id'])
        productos.nombre_proveedor = nombre_proveedor.nombre_proveedor

    if data['id_categoria_id']:
        id_categoria = Categorias.objects.only("id_categoria").get(id_categoria = data['id_categoria_id'])
        productos.id_categoria = id_categoria
        nombre_categoria = Categorias.objects.only("categoria").get(id_categoria = data['id_categoria_id'])
        productos.categoria = nombre_categoria.categoria

    

    productos.nombre_producto = data['nombre_producto']
    productos.costo = data['costo']
    productos.medidas = data['medidas']
    productos.tiempo_entrega = data['tiempo_entrega']
    productos.nota = data['nota']
    productos.save()

    productos = Productos.objects.filter(id_producto = id_producto)
    return Response(productos.values())

@api_view(['DELETE'])
def EliminarProducto(request, **kwargs):
    id_producto = kwargs['pk']
    producto = Productos.objects.get(id_producto = id_producto)
    producto.delete()
    return Response({"El producto fue eliminado"})

    