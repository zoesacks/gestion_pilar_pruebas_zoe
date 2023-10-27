from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import factura, codigoUsado, codigoAprobacion, ordenDePago
from administracion.models import codigoFinanciero
from contaduria.models import proyeccionGastos
from django.utils import timezone
from datetime import datetime
from django.db.models.functions import ExtractMonth
import datetime
from django.db.models import Sum
from administracion.gestion_pases import contaduria_required
from django.contrib.auth.models import User
import json
from decimal import Decimal

meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
codigoIngresado = ""

@contaduria_required
def detalleFactura(request, factura_detalle_id):
    factura_detalle = factura.objects.get(pk=factura_detalle_id)
    op = None

    if ordenDePago.objects.filter(nroFactura = factura_detalle.nroFactura, proveedor = factura_detalle.proveedor).exists():
        op = ordenDePago.objects.get(nroFactura = factura_detalle.nroFactura, proveedor = factura_detalle.proveedor)


    totalDisponible = obtenerDineroDisponible(factura_detalle.codigo.CODIGO)

    if request.method == 'POST':

        if 'factura_button_id' in request.POST:
            autorizarFactura(request)

        return redirect('facturas')


    context = {
        'factura' : factura_detalle,
        'totalDisponible': totalDisponible,
        'ordenDePago': op,
    }

    return render(request, 'factura_detalle.html', context)

@contaduria_required
def facturas(request):

    #filtra por proveedor, por factura y por facturas autorizadas y no autorizadas
    facturas = filtrar(request)
    
    #Listado de proveedores y facturas sin repetidos
    proveedores = facturas.values_list('proveedor', flat=True).distinct()
    nroFacturas = facturas.values_list('nroFactura', flat=True).distinct()
    
    cantidad_facturas_pendientes = facturas.count()

    montoCodigoAprobacion =  0
    
    if request.method == 'POST':
        #cambio el estado de una sola factura
        if 'factura_button_id' in request.POST:
            autorizarFactura(request)

        #cambio el estado de una sola factura
        if 'factura_desautorizar' in request.POST:
            desautorizarFactura(request)

        #cambio el estado si se apreto el boton de autorizar
        if 'autorizar_seleccionados' in request.POST:
            autorizarSelccionados(request)

        #si se apreto el boton para ver el detalle
        if 'factura_detalle_id' in request.POST:
            factura_detalle_id = request.POST.get('factura_detalle_id')
            return redirect('detalleFactura', factura_detalle_id = factura_detalle_id)  

        #si se ingresa un codigo se obtiene el monto que queda del mismo
        if 'ingresarCodigo' in request.POST:
            montoCodigoAprobacion = obtenerMontoCodigo(request) or 0

        if 'ingresarCodigoMod' in request.POST:
            montoCodigoAprobacion = obtenerMontoCodigoModal(request) or 0

    totalDisponibleConCodigo = {}
    totalDisponible = {}
    total = 0
    grupos_usuario = request.user.groups.values_list('name', flat=True)

    for codigo in grupos_usuario: 
        totalDisponibleConCodigo[codigo] = obtenerDineroDisponible(codigo)  + montoCodigoAprobacion
        totalDisponible[codigo] = obtenerDineroDisponible(codigo)
        total += totalDisponible[codigo]

    totalDisponible_json = json.dumps(totalDisponibleConCodigo)
    total += montoCodigoAprobacion


    # Agrega esta línea para definir la cantidad de elementos por página
    items_por_pagina = 100
    paginator = Paginator(facturas, items_por_pagina)
    
    # Agrega el parámetro "page" para obtener la página deseada (por ejemplo, ?page=2)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    
    context = {
        'page' : page,
        'cantidad_facturas_pendientes' : cantidad_facturas_pendientes,
        'proveedores':proveedores,
        'nroFacturas' : nroFacturas,
        'totalDisponible': totalDisponible,
        'totalDisponible_json': totalDisponible_json,
        'montoCodigoAprobacion': montoCodigoAprobacion,
        'totalDisponibleConCodigo' : totalDisponibleConCodigo,
        'total' : total,
    }

    return render(request, 'facturas.html', context)


def filtrar(request):
    facturas = factura.objects.all()

    #grupo = request.user.groups.first()
    grupos_usuario = request.user.groups.values_list('name', flat=True)

    facturas = facturas.filter(codigo__CODIGO__in=grupos_usuario, estado='Pendiente')
    #facturas = facturas.filter(codigo__CODIGO = grupo, estado = 'Pendiente')

    # Obtener los parámetros de los filtros (si están presentes)
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    proveedores_seleccionados = request.GET.getlist('proveedor')
    facturas_seleccionadas = request.GET.getlist('nroFactura')
    verFacturas = request.GET.get('verFacturas')
    
    if verFacturas:
        if verFacturas == "autorizadas":
            facturas = factura.objects.filter(codigo__CODIGO__in=grupos_usuario, estado = 'Autorizado')

        elif verFacturas == "op":
            facturas = factura.objects.filter(codigo__CODIGO__in=grupos_usuario, estado = 'OP')

        else: 
            facturas = facturas.filter(codigo__CODIGO__in=grupos_usuario, estado = 'Pendiente')

    # Aplicar los filtros si están presentes
    if fecha_desde and fecha_hasta:
        # Convertir las fechas de texto a objetos datetime
        fecha_desde = datetime.datetime.strptime(fecha_desde, '%Y-%m-%d').date()
        fecha_hasta = datetime.datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
        # Filtrar por rango de fechas
        facturas = facturas.filter(emision__range=(fecha_desde, fecha_hasta))

    if proveedores_seleccionados:
        #filtar por proveedores seleccionados
        facturas = facturas.filter(proveedor__in = proveedores_seleccionados)

    if facturas_seleccionadas:
        #filtrar por facturas
        facturas = facturas.filter(nroFactura__in = facturas_seleccionadas)

    return facturas

def obtenerMontoCodigo(request):
    global codigoIngresado
    codigoIngresado = request.POST.get('codigoAutorizacion')

    montoCodigoAprobacion = 0

    if codigoAprobacion.objects.filter(codigoApro = codigoIngresado).exists():  
        montoCodigoAprobacion = codigoAprobacion.objects.get(codigoApro = codigoIngresado).monto or 0
        totalUsado = codigoUsado.objects.filter(codigo__codigoApro = codigoIngresado).aggregate(total=Sum('montoUsado'))['total'] or 0
        montoCodigoAprobacion -= totalUsado


    return float(round(montoCodigoAprobacion, 2))

def obtenerMontoCodigoModal(request):
    global codigoIngresado
    codigoIngresado = request.POST.get('codigoAutorizacionMod')
    montoCodigoAprobacion = 0

    if codigoAprobacion.objects.filter(codigoApro = codigoIngresado).exists():  
        montoCodigoAprobacion = codigoAprobacion.objects.get(codigoApro = codigoIngresado).monto or 0
        totalUsado = codigoUsado.objects.filter(codigo__codigoApro = codigoIngresado).aggregate(total=Sum('montoUsado'))['total'] or 0
        montoCodigoAprobacion -= totalUsado

    return float(round(montoCodigoAprobacion, 2))

def obtenerDineroDisponible(codigo):

    totalUsado = 0

    #obtengo el total de dinero que se uso con los codigoAprobacion
    codigosUsados = codigoUsado.objects.filter(codigoFinanciero__CODIGO = codigo, fecha__month = ExtractMonth(timezone.now()))
    totalUsado = codigosUsados.aggregate(total=Sum('montoUsado'))['total'] or 0

    

    #obtengo el dinero disponible del mes
    proyeccion = proyeccionGastos.objects.filter(CODIGO=codigo, MES = datetime.datetime.now().month, EJERCICIO = datetime.datetime.now().year)
    totalDisponible = proyeccion.aggregate(total=Sum('IMPORTE'))['total'] or 0

    #obtengo el dinero total de las facturas autorizadas del mes
    facturasAutorizadas = factura.objects.filter(codigo__CODIGO=codigo, estado = 'Autorizado', autorizado_fecha__month = ExtractMonth(timezone.now()))
    totalFacturasAutorizadas = facturasAutorizadas.aggregate(total=Sum('total'))['total'] or 0
    
    totalDisponible = float(round(totalDisponible - totalFacturasAutorizadas  + totalUsado, 2))

    return totalDisponible

def autorizarSelccionados(request):
        #obtengo lista de todos los que se hicieron check
    facturas_check_id = request.POST.getlist('facturas_check_id')

    for factura_check_id in facturas_check_id:
        factura_selec = factura.objects.get(pk=factura_check_id)
        factura_selec.autorizado_por = request.user.username
        factura_selec.autorizado_fecha = timezone.now() - timezone.timedelta(hours=3)
        factura_selec.estado = 'Autorizado'

        codigo = factura_selec.codigo.CODIGO
        
        if obtenerDineroDisponible(codigo) < factura_selec.total:

            global codigoIngresado
            #agrego los datos de quien uso el codigo
            codigoU = codigoUsado()
            codigoU.codigo = codigoAprobacion.objects.get(codigoApro = codigoIngresado) 
            codigoU.factura = factura_selec
            codigoU.codigoFinanciero = codigoFinanciero.objects.get(CODIGO = codigo)
            codigoU.montoUsado  = float(factura_selec.total) - obtenerDineroDisponible(codigo)
            codigoU.usuario = request.user.username
            codigoU.fecha = timezone.now() - timezone.timedelta(hours=3)

            codigoU.save()

        factura_selec.save()
            
    return redirect('facturas')

def desautorizarFactura(request):

    #obtengo el id del que se apreto el boton para marcar como Autorizado
    factura_desautorizar = request.POST.get('factura_desautorizar')

    factura_selec = factura.objects.get(pk=factura_desautorizar)
    factura_selec.autorizado_por = None
    factura_selec.autorizado_fecha = None
    factura_selec.estado = 'Pendiente'

    if codigoUsado.objects.filter(factura = factura_selec).exists():
        codigosUsados = codigoUsado.objects.filter(factura = factura_selec)

        for codigo in codigosUsados:
            codigo.delete()
            
    factura_selec.save()
    return redirect('facturas')

def autorizarFactura(request):

    #obtengo el id del que se apreto el boton para marcar como Autorizado
    factura_button_id = request.POST.get('factura_button_id')

    factura_selec = factura.objects.get(pk=factura_button_id)
    factura_selec.autorizado_por = request.user.username
    factura_selec.autorizado_fecha = timezone.now() - timezone.timedelta(hours=3)
    factura_selec.estado = 'Autorizado'
    
    codigo = factura_selec.codigo.CODIGO

    totalDisponible = obtenerDineroDisponible(codigo)

    if totalDisponible < factura_selec.total:
        global codigoIngresado
        
        #agrego los datos de quien uso el codigo
        codigoU = codigoUsado()
        codigoU.codigo = codigoAprobacion.objects.get(codigoApro = codigoIngresado) 
        codigoU.factura = factura_selec
        codigoU.codigoFinanciero = factura_selec.codigo
        codigoU.montoUsado  = float(factura_selec.total) - totalDisponible
        codigoU.usuario = request.user.username
        codigoU.fecha = timezone.now() - timezone.timedelta(hours=3)

        codigoU.save()
    
    factura_selec.save()

    return redirect('facturas')