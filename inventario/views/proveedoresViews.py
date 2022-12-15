from rest_framework.response                         import Response
from rest_framework.decorators                       import api_view

from inventario.models import Proveedores

@api_view(['GET'])
def VerProveedores(request):
    proveedores    = Proveedores.objects.all()
    return Response(proveedores.values())

@api_view(['POST'])
def CrearProveedores(request, *args, **kwargs):
    data = request.data
    proveedor = Proveedores.objects.create(
        nombre_proveedor = data['nombre_proveedor'],
        telefono_proveedor = data['telefono_proveedor'],
        segundo_telefono = data['segundo_telefono'],
        direccion_proveedor = data['direccion_proveedor'],
        observacion = data['observacion'],
    )
    id_proveedor = proveedor.id_proveedor
    proveedor.save()
    proveedor = Proveedores.objects.filter(id_proveedor = id_proveedor)
    return Response(proveedor.values())

@api_view(['PUT'])
def EditarProveedor(request, **kwargs):
    id_proveedor = kwargs['pk']
    data = request.data
    
    proveedor = Proveedores.objects.get(id_proveedor = id_proveedor)
    proveedor.nombre_proveedor = data['nombre_proveedor']
    proveedor.telefono_proveedor = data['telefono_proveedor']
    proveedor.segundo_telefono = data['segundo_telefono']
    proveedor.direccion_proveedor = data['direccion_proveedor']
    proveedor.observacion = data['observacion']
    proveedor.save()

    proveedor = Proveedores.objects.filter(id_proveedor = id_proveedor)
    return Response(proveedor.values())

@api_view(['DELETE'])
def EliminarProveedor(request, **kwargs):
    id_proveedor = kwargs['pk']
    proveedor = Proveedores.objects.get(id_proveedor = id_proveedor)
    proveedor.delete()
    return Response({"El proveedor fue eliminado."})