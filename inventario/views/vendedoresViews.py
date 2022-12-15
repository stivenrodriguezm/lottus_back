from rest_framework                                  import views
from rest_framework.response                         import Response
from rest_framework.decorators                       import api_view

from inventario.models import Vendedores

@api_view(['GET'])
def VerVendedores(request):
    vendedores = Vendedores.objects.all()
    return Response(vendedores.values())

@api_view(['POST'])
def CrearVendedor(request, *args, **kwargs):
    data = request.data
    vendedor = Vendedores.objects.create(
        nombre_vendedor = data['nombre_vendedor'],
        telefono_vendedor = data['telefono_vendedor'],
        cedula_vendedor = data['cedula_vendedor'],
        correo_vendedor = data['correo_vendedor'],
        direccion_vendedor = data['direccion_vendedor'],
        activo = data['activo'],
        nombre_contacto_emergencia = data['nombre_contacto_emergencia'],
        numero_contacto_emergencia = data['numero_contacto_emergencia']
    )
    id_vendedor = vendedor.id_vendedor
    vendedor.save()
    vendedor = Vendedores.objects.filter(id_vendedor = id_vendedor)
    return Response(vendedor.values())

@api_view(['PUT'])
def EditarVendedor(request, **kwargs):
    id_vendedor = kwargs['pk']
    data = request.data
    vendedor = Vendedores.objects.get(id_vendedor = id_vendedor)
    vendedor.nombre_vendedor = data['nombre_vendedor']
    vendedor.telefono_vendedor = data['telefono_vendedor']
    vendedor.cedula_vendedor = data['cedula_vendedor']
    vendedor.correo_vendedor = data['correo_vendedor']
    vendedor.direccion_vendedor = data['direccion_vendedor']
    vendedor.activo = data['activo']
    vendedor.nombre_contacto_emergencia = data['nombre_contacto_emergencia']
    vendedor.numero_contacto_emergencia = data['numero_contacto_emergencia']
    vendedor.save()

    vendedor = Vendedores.objects.filter(id_vendedor = id_vendedor)
    return Response(vendedor.values())

@api_view(['DELETE'])
def EliminarVendedor(request, **kwargs):
    id_vendedor = kwargs['pk']
    vendedor = Vendedores.objects.get(id_vendedor = id_vendedor)
    vendedor.delete()
    return Response({"El vendedor fue eliminado"})