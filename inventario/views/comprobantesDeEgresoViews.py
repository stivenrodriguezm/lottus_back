from multiprocessing.dummy import Array
from rest_framework                                  import views
from rest_framework.response                         import Response
from rest_framework.decorators                       import api_view

from inventario.models import ComprobantesDeEgreso, Caja, ValorEnCaja, Proveedores, Facturas, Bancos, CadaBanco
from django.db import connection

import ast


@api_view(['GET'])
def VerCEs(request):
    comprobante = ComprobantesDeEgreso.objects.all()
    return Response(comprobante.values())

@api_view(['POST'])
def CrearCE(request):
    data = request.data

    #crear comprobante de egreso 
    proveedor = Proveedores.objects.only("id_proveedor").get(id_proveedor = data['id_proveedor'])
    comprobante = ComprobantesDeEgreso.objects.create(
        numero_comprobante_egreso = data['numero_comprobante_egreso'],
        fecha = data['fecha'],
        id_proveedor = proveedor,
        metodo_pago = data['metodo_pago'],
        valor = data['valor'],
        facturas = data['facturas'],
    )
    numero_comprobante_egreso = comprobante.numero_comprobante_egreso
    id_auto = comprobante.id_auto
    facturas = comprobante.facturas
    comprobante.save()

    # facturas = ast.literal_eval(facturas)
    facturas = facturas.split(",")

    # iterar entre las facturas y actualizarlas a pagadas guardandoles el # de CE.
    for factura in facturas:
        fact = Facturas.objects.get(id_auto = int(factura))
        fact.pagada = True
        fact.save()


    #Crear movimieno en caja y sumar a saldo actual en caja
    metodo_pago = data['metodo_pago']
    if metodo_pago == "Efectivo":
        caja = Caja.objects.create(
            fecha = data['fecha'],
            concepto = str(data['numero_comprobante_egreso']),
            tipo = 'Egreso',
            subtipo = 'Egresos con RC.',
            valor = data['valor'],
        )
        id_movimiento = caja.id_movimiento
        tipo = caja.tipo
        valor = caja.valor
        caja.save()

        valorCajaData = ValorEnCaja.objects.get(id = 1)
        valorCaja = valorCajaData.valorActual
        
        if tipo == "Ingreso":
            valorCaja = valorCaja + valor
        if tipo == "Egreso":
            valorCaja = valorCaja - valor
        if tipo == "Cierre":
            valorCaja = valorCaja

        valorCajaData.valorActual = valorCaja
        valorCajaData.save()

        caja = Caja.objects.get(id_movimiento = id_movimiento)
        caja.valorCaja = valorCaja
        caja.save()
        id_caja = Caja.objects.only("id_movimiento").get(id_movimiento = id_movimiento)
        comprobante.id_movimiento_caja = id_caja

    if metodo_pago == "Transferencia":
        # Agregar movimiento bancario a Bancos (Movimientos bancarios)
        movimiento_banco = Bancos.objects.create(
            banco = data['banco'],
            concepto = f'CE. {numero_comprobante_egreso}',
            fecha = data['fecha'],
            tipo = "Ingreso",
            valor = data['valor'],
        )
        id_movimiento = movimiento_banco.id_movimiento
        tipo = movimiento_banco.tipo
        banco = movimiento_banco.banco
        valor = movimiento_banco.valor
        movimiento_banco.save()

        # Restar el valor del movimiento bancario en el banco correspondiente en CadaBanco y total_bancos
        cadaBanco = CadaBanco.objects.get(id_auto = 1)
        if banco == "bancolombia_lottus":
            cadaBanco.total_bancos = cadaBanco.total_bancos - valor
            cadaBanco.bancolombia_lottus = cadaBanco.bancolombia_lottus - valor
            cadaBanco.save()


        id_mov_bancos = Bancos.objects.only("id_movimiento").get(id_movimiento = id_movimiento)
        comprobante.id_movimiento_bancos = id_mov_bancos

    
    comprobante.save()


    comprobantePrint = ComprobantesDeEgreso.objects.filter(id_auto = id_auto)

    return Response(comprobantePrint.values())
    


@api_view(['DELETE'])
def EliminarCE(request, **kwargs):
    id_auto = kwargs['pk']
    egreso = ComprobantesDeEgreso.objects.get(id_auto = id_auto)

    valor = egreso.valor

    #iterar entre las facturas de ese C.E. y marcarlas como NO pagas
    facturas = egreso.facturas
    facturas = ast.literal_eval(facturas)
    
    for factura in facturas:
        fact = Facturas.objects.get(id_auto = int(factura))
        fact.pagada = False
        fact.save()

    # Restar valor en caja
    valorCajaData = ValorEnCaja.objects.get(id = 1)
    valorCaja = valorCajaData.valorActual

    if egreso.metodo_pago == 'Efectivo': 
        valorCaja = valorCaja + valor

    valorCajaData.valorActual = valorCaja
    valorCajaData.save()

    # Eliminar entrada de caja
    caja = Caja.objects.get(id_movimiento = egreso.id_movimiento_caja_id)
    caja.delete()


    # El comprobante de egreso se elimina gracias al modelo cascada al eliminar la entrada de caja

    return Response({'Eliminado correctamente'})
