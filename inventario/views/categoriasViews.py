from rest_framework import views
from rest_framework.response import Response
from rest_framework.decorators import api_view

from inventario.models import Categorias

@api_view(['GET'])
def VerCategorias(request):
    categorias    = Categorias.objects.all()
    return Response(categorias.values())

@api_view(['POST'])
def CrearCategoria(request, *args, **kwargs):
    data = request.data
    categoria = Categorias.objects.create(
        categoria = data['categoria']
    )
    id_categoria = categoria.id_categoria
    categoria.save()
    categoria = Categorias.objects.filter(id_categoria = id_categoria)
    return Response(categoria.values())

@api_view(['PUT'])
def EditarCategoria(request, **kwargs):
    id_categoria = kwargs['pk']
    data = request.data
    
    categoria = Categorias.objects.get(id_categoria = id_categoria)
    categoria.categoria = data['categoria']
    categoria.save()

    categoria = Categorias.objects.filter(id_categoria = id_categoria)
    return Response(categoria.values())

@api_view(['DELETE'])
def EliminarCategoria(request, **kwargs):
    id_categoria = kwargs['pk']
    categoria = Categorias.objects.get(id_categoria = id_categoria)
    categoria.delete()
    return Response({"La categoria fue eliminada."})