from rest_framework                                  import views
from rest_framework.response                         import Response
from rest_framework.decorators                       import api_view

from inventario.models import Pedidos

@api_view(['GET'])
def VerOrdenesPedido(request):
    pedido = Pedidos.objects.all()
    return Response(pedido.values())

@api_view(['POST'])
def CrearOrdenPedido(request, *args, **kwargs):
    data = request.data
    pedido = Pedidos.objects.create(
        id_orden_pedido = data['id_orden_pedido'],
        id_venta = data['id_venta'],
        id_proveedor = data['id_proveedor'],
        id_vendedor = data['id_vendedor'],
        fecha = data['fecha'],
        fecha_despacho = data['fecha_despacho'],
        tela = data['tela'],
        enviada = data['enviada'],
        recibida = data['recibida']
    )
    pedido.save()
    return Response({"Pedido creado exitosamente."})

@api_view(['PUT'])
def EditarOrdenPedido(request, **kwargs):
    id_auto = kwargs['pk']
    data = request.data
    pedido = Pedidos.objects.get(id_auto = id_auto)
    pedido.id_orden_pedido = data['id_orden_pedido']
    pedido.id_venta = data['id_venta']
    pedido.id_proveedor = data['id_proveedor']
    pedido.id_vendedor = data['id_vendedor']
    pedido.fecha = data['fecha']
    pedido.fecha_despacho = data['fecha_despacho']
    pedido.tela = data['tela']
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