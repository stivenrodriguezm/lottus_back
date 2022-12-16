from rest_framework                                  import views
from rest_framework.response                         import Response
from rest_framework.decorators                       import api_view

from inventario.models import Ventas, Vendedores, Clientes

@api_view(['GET'])
def VerVentas(request):
    ventas = Ventas.objects.all()
    return Response(ventas.values())

@api_view(['POST'])
def CrearVenta(request, *args, **kwargs):
    data = request.data
    cliente = Clientes.objects.create(
        nombre_cliente = data['nombre_cliente'],
        cedula_cliente = data['cedula_cliente'],
        direccion_cliente = data['direccion_cliente'],
        ciudad_cliente = data['ciudad_cliente'],
        correo_cliente = data['correo_cliente'],
        telefono_cliente = data['telefono_cliente'],
    )
    id_cliente = cliente.id_cliente
    cliente.save()
    cliente = Clientes.objects.only('id_cliente').get(id_cliente = id_cliente)
    vendedor = Vendedores.objects.only("id_vendedor").get(id_vendedor = data['id_vendedor'])
    nombre_vendedor = Vendedores.objects.filter(id_vendedor = data['id_vendedor'])
    venta = Ventas.objects.create(
        id_venta = data['id_venta'],
        id_vendedor = vendedor,
        nombre_vendedor = nombre_vendedor[0].nombre_vendedor,
        fecha_venta = data['fecha_venta'],
        fecha_entrega = data['fecha_entrega'],
        id_cliente = cliente,
        nombre_cliente = data['nombre_cliente'],
        cedula_cliente = data['cedula_cliente'],
        entregado = data['entregado'],
        valor_venta = data['valor_venta'],
        saldo = data['valor_venta']
    )
    id_auto = venta.id_auto
    venta.save()
    venta = Ventas.objects.filter(id_auto = id_auto)
    return Response(venta.values())

@api_view(['PUT'])
def EditarVenta(request, **kwargs):
    id_auto = kwargs['pk']
    data = request.data
    vendedor = Vendedores.objects.only("id_vendedor").get(id_vendedor = data['id_vendedor_id'])
    venta = Ventas.objects.get(id_auto = id_auto)

    if(vendedor != venta.id_vendedor):
        venta.id_vendedor = vendedor
        name = Vendedores.objects.get(id_vendedor = vendedor.id_vendedor)
        venta.nombre_vendedor = name.nombre_vendedor

    if(venta.valor_venta != data['valor_venta']):
        abono = venta.abono
        valor_venta = data['valor_venta']
        if (abono == None):
            venta.valor_venta = valor_venta
            venta.saldo = valor_venta
        else:
            nuevo_saldo = valor_venta - abono                      
            venta.valor_venta = valor_venta
            venta.saldo = nuevo_saldo

    venta.id_venta = data['id_venta']
    venta.fecha_venta = data['fecha_venta']
    venta.fecha_entrega = data['fecha_entrega']
    venta.entregado = data['entregado']
    venta.save()

    venta = Ventas.objects.filter(id_auto = id_auto)
    return Response(data)

@api_view(['DELETE'])
def EliminarVenta(request, **kwargs):
    id_auto = kwargs['pk']
    venta = Ventas.objects.get(id_auto = id_auto)
    venta.delete()
    return Response({"La venta fue eliminada"})