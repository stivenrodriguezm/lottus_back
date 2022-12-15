from rest_framework                                  import views
from rest_framework.response                         import Response
from rest_framework.decorators                       import api_view

from inventario.models import Transportadores

@api_view(['GET'])
def VerTransportadores(request):
    transportadores = Transportadores.objects.all()
    return Response(transportadores.values())

@api_view(['POST'])
def CrearTransportador(request, *args, **kwargs):
    data = request.data
    transportador = Transportadores.objects.create(
        nombre_transportador = data['nombre_transportador'],
        telefono_transportador = data['telefono_transportador'],
        cedula_transportador = data['cedula_transportador'],
        direccion_transportador = data['direccion_transportador'],
        nombre_contacto_emergencia = data['nombre_contacto_emergencia'],
        numero_contacto_emergencia = data['numero_contacto_emergencia']
    )
    id_transportador = transportador.id_transportador
    transportador.save()
    transportador = Transportadores.objects.filter(id_transportador = id_transportador)
    return Response(transportador.values())

@api_view(['PUT'])
def EditarTransportador(request, **kwargs):
    id_transportador = kwargs['pk']
    data = request.data
    transportador = Transportadores.objects.get(id_transportador = id_transportador)
    transportador.nombre_transportador = data['nombre_transportador']
    transportador.telefono_transportador = data['telefono_transportador']
    transportador.cedula_transportador = data['cedula_transportador']
    transportador.direccion_transportador = data['direccion_transportador']
    transportador.nombre_contacto_emergencia = data['nombre_contacto_emergencia']
    transportador.numero_contacto_emergencia = data['numero_contacto_emergencia']
    transportador.save()

    transportador = Transportadores.objects.filter(id_transportador = id_transportador)
    return Response(transportador.values())

@api_view(['DELETE'])
def EliminarTransportador(request, **kwargs):
    id_transportador = kwargs['pk']
    transportador = Transportadores.objects.get(id_transportador = id_transportador)
    transportador.delete()
    return Response({"El transportador fue eliminado"})