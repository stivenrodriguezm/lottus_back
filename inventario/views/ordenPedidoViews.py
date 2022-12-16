from rest_framework                                  import views
from rest_framework.response                         import Response
from rest_framework.decorators                       import api_view

from inventario.models import Pedidos, Ventas, Proveedores, Vendedores

@api_view(['GET'])
def VerOrdenesPedido(request):
    pedido = Pedidos.objects.all()
    return Response(pedido.values())

@api_view(['POST'])
def CrearOrdenPedido(request, *args, **kwargs):
    data = request.data
    venta = Ventas.objects.only("id_venta").get(id_auto = data['id_venta'])
    proveedor = Proveedores.objects.only("id_proveedor").get(id_proveedor = data['id_proveedor'])
    vendedor = Vendedores.objects.only("id_vendedor").get(id_vendedor = data['id_vendedor'])
    pedido = Pedidos.objects.create(
        id_orden_pedido = data['id_orden_pedido'],
        id_venta = venta,
        id_proveedor = proveedor,
        id_vendedor = vendedor,
        fecha = data['fecha'],
        fecha_despacho = data['fecha_despacho'],
        tela = data['tela'],
        enviada = data['enviada'],
        recibida = data['recibida'],
        valor_total = data['valor_total']
    )
    id_auto = pedido.id_auto
    pedido.save()
    pedido = Pedidos.objects.filter(id_auto = id_auto)
    return Response(pedido.values())

@api_view(['PUT'])
def EditarOrdenPedido(request, **kwargs):
    id_auto = kwargs['pk']
    data = request.data

    venta = Ventas.objects.only("id_venta").get(id_auto = data['id_venta'])
    proveedor = Proveedores.objects.only("id_proveedor").get(id_proveedor = data['id_proveedor'])
    vendedor = Vendedores.objects.only("id_vendedor").get(id_vendedor = data['id_vendedor'])

    pedido = Pedidos.objects.get(id_auto = id_auto)
    pedido.id_orden_pedido = data['id_orden_pedido']
    pedido.valor_total = data['valor_total']
    pedido.id_venta = venta
    pedido.id_proveedor = proveedor
    pedido.id_vendedor = vendedor
    pedido.tela = data['tela']
    pedido.fecha = data['fecha']
    pedido.fecha_despacho = data['fecha_despacho']
    pedido.enviada = data['enviada']
    pedido.recibida = data['recibida']
    pedido.save()

    pedido = Pedidos.objects.filter(id_auto = id_auto)
    return Response(pedido.values())
    

@api_view(['DELETE'])
def EliminarOrdenPedido(request, **kwargs):
    id_auto = kwargs['pk']
    pedido = Pedidos.objects.get(id_auto = id_auto)
    pedido.delete()
    return Response({"El pedido fue eliminado."})