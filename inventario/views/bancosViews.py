from rest_framework                                  import views
from rest_framework.response                         import Response
from rest_framework.decorators                       import api_view

from inventario.models import CadaBanco, Bancos
from django.db import connection


@api_view(['GET'])
def VerSaldoBancos(request):
    bancos_saldo = CadaBanco.objects.all()
    return Response(bancos_saldo.values())
@api_view(['GET'])
def VerMovimientosBancos(request):
    bancos_movimientos = Bancos.objects.all()
    return Response(bancos_movimientos.values())

@api_view(['POST'])
def AgregarSaldoBancos(request):
    data = request.data

    # Agregar movimiento bancario a Bancos (Movimientos bancarios)
    movimiento = Bancos.objects.create(
        banco = data['banco'],
        concepto = data['concepto'],
        fecha = data['fecha'],
        tipo = data['tipo'],
        valor = data['valor'],
    )
    tipo = movimiento.tipo
    banco = movimiento.banco
    valor = movimiento.valor
    movimiento.save()

    # Sumar o restar el valor del movimiento bancario en el banco correspondiente en CadaBanco
    if banco == "bancolombia_lottus":
        cadaBanco = CadaBanco.objects.get(id_auto = 1)
        if tipo == "Ingreso":
            cadaBanco.total_bancos = cadaBanco.total_bancos + valor
            cadaBanco.bancolombia_lottus = cadaBanco.bancolombia_lottus + valor
            cadaBanco.save()
        if tipo == "Egreso":
            cadaBanco.total_bancos = cadaBanco.total_bancos - valor
            cadaBanco.bancolombia_lottus = cadaBanco.bancolombia_lottus - valor
            cadaBanco.save()
    if banco == "bancolombia_stiven":
        cadaBanco = CadaBanco.objects.get(id_auto = 1)
        if tipo == "Ingreso":
            cadaBanco.total_bancos = cadaBanco.total_bancos + valor
            cadaBanco.bancolombia_stiven = cadaBanco.bancolombia_stiven + valor
            cadaBanco.save()
        if tipo == "Egreso":
            cadaBanco.total_bancos = cadaBanco.total_bancos - valor
            cadaBanco.bancolombia_stiven = cadaBanco.bancolombia_stiven - valor
            cadaBanco.save()
    if banco == "davivienda":
        cadaBanco = CadaBanco.objects.get(id_auto = 1)
        if tipo == "Ingreso":
            cadaBanco.total_bancos = cadaBanco.total_bancos + valor
            cadaBanco.davivienda = cadaBanco.davivienda + valor
            cadaBanco.save()
        if tipo == "Egreso":
            cadaBanco.total_bancos = cadaBanco.total_bancos - valor
            cadaBanco.davivienda = cadaBanco.davivienda - valor
            cadaBanco.save()
    if banco == "nequi":
        cadaBanco = CadaBanco.objects.get(id_auto = 1)
        if tipo == "Ingreso":
            cadaBanco.total_bancos = cadaBanco.total_bancos + valor
            cadaBanco.nequi = cadaBanco.nequi + valor
            cadaBanco.save()
        if tipo == "Egreso":
            cadaBanco.total_bancos = cadaBanco.total_bancos - valor
            cadaBanco.nequi = cadaBanco.nequi - valor
            cadaBanco.save()
    if banco == "daviplata":
        cadaBanco = CadaBanco.objects.get(id_auto = 1)
        if tipo == "Ingreso":
            cadaBanco.total_bancos = cadaBanco.total_bancos + valor
            cadaBanco.daviplata = cadaBanco.daviplata + valor
            cadaBanco.save()
        if tipo == "Egreso":
            cadaBanco.total_bancos = cadaBanco.total_bancos - valor
            cadaBanco.daviplata = cadaBanco.daviplata - valor
            cadaBanco.save()




    return Response({"agrego?"})
