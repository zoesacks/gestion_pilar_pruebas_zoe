
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import solped,productoPedido,mesa
from django.db.models import Sum
from django.core.paginator import Paginator, Page
from datetime import datetime
import datetime
from django.utils import timezone
from administracion.gestion_pases import contaduria_required

@contaduria_required
def autorizar_solicitudes(request):
    if request.method == 'POST':
        
        solicitud_id = solicitud_id
        solicitudes_seleccionadas = request.POST.getlist('solicitudes[]')

        for solicitud_id in solicitudes_seleccionadas:
            try:
                solicitud = solped.objects.get(pk=solicitud_id)
                solicitud.ESTADO = 1
                solicitud.AUTORIZADO_POR = request.user.username
                solicitud.FECHA_AUTORIZADO = timezone.now() - timezone.timedelta(hours=3)
                solicitud.save()
            except solped.DoesNotExist:
                pass

    return redirect('solicitudes')  # Redirige nuevamente a la lista de solicitudes


@contaduria_required
def detalle_solicitud(request):
    
    if request.method == "POST":
        
        solicitud_id = request.POST.get('solicitud_id')
        solicitud_id_observacion = request.POST.get('solicitud_id_observacion')

        if solicitud_id_observacion:
            try:
                solicitud = solped.objects.get(pk=solicitud_id)
                solicitud.COMENTARIOS = "Observada"
                solicitud.save()
                
                context = {
                    'solicitud': solicitud, 
                    'articulos':articulos,
                    'solicitud_id':solicitud.id,
                    }
                
                return render(request, 'solicitudes_detalle.html', context)
            
            except solped.DoesNotExist:
                pass

        else:
            try:
                solicitud = solped.objects.get(pk=solicitud_id)
                articulos = productoPedido.objects.all().filter(pedido=solicitud_id)


                context = {
                    'solicitud': solicitud, 
                    'articulos':articulos,
                    'solicitud_id':solicitud_id,
                    }
                
                return render(request, 'solicitudes_detalle.html', context)
            
            except solped.DoesNotExist:
                pass
    return HttpResponse("Error al cargar los detalles de la solicitud")


@contaduria_required
def solicitudes_list(request):


    if request.method == 'POST':
         
        solicitud_id = request.POST.get('solicitud_id')
        solicitud_id_observacion = request.POST.get('solicitud_id_observacion')
        solicitudes_seleccionadas = request.POST.getlist('solicitudes_seleccionadas')
        ver_solicitudes = request.POST.getlist('ver_solicitudes')
        

        if solicitud_id_observacion:
            solicitud = solped.objects.get(pk=solicitud_id_observacion)
            solicitud.COMENTARIOS = "Observada"
            solicitud.save()
            return redirect('solicitudes')

        elif solicitud_id:
            solicitud = solped.objects.get(pk=solicitud_id)
            solicitud.ESTADO = 1
            solicitud.AUTORIZADO_POR = request.user.username
            solicitud.FECHA_AUTORIZADO = timezone.now() - timezone.timedelta(hours=3)
            solicitud.save()
            return redirect('solicitudes')
      
        elif solicitudes_seleccionadas:
            
            # Iterar sobre los IDs y procesar cada solicitud
            for solicitud_id in solicitudes_seleccionadas:

                solicitudes_select = str(solicitud_id).split(",")

                for x in solicitudes_select:

                    try:
                        # Obtener la solicitud correspondiente por su ID
                        solicitud = solped.objects.get(id=x)

                        # Realizar las operaciones deseadas en la solicitud (por ejemplo, actualizar el campo ESTADO)
                        solicitud.ESTADO = 1
                        solicitud.AUTORIZADO_POR = request.user.username
                        solicitud.FECHA_AUTORIZADO = timezone.now() - timezone.timedelta(hours=3)
                        solicitud.save()

                        #print(f'Solicitud aprobada. solicitud id:{solicitud.id}')

                    except (ValueError, solped.DoesNotExist) as ex:
                        # Manejar casos donde el ID no sea válido o no se encuentre la solicitud
                        #print(ex)
                        pass

            return redirect('solicitudes')

        elif ver_solicitudes:
            solicitudes = solped.objects.all()

            context = {'solicitudes': solicitudes}
            return render(request, 'solicitudes_list.html', context)
        
    solicitudes = solped.objects.all().order_by('ESTADO','-OBSERVADA',).filter(ESTADO=0)
        
    ##FILTROS
    #Listado de secretarias y ff sin repetidos
    secretariasListado = solped.objects.all().values_list('SECRETARIA_NOMBRE', flat=True).distinct()
    fondosFinanciamiento = solped.objects.all().values_list('FUENTE_FINANCIAMIENTO', flat=True).distinct()

    # Obtener los parámetros de los filtros (si están presentes)
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    secretarias_seleccionados = request.GET.getlist('secre')
    ff_seleccionadas = request.GET.getlist('ff')
    verSolicitudes = request.GET.get('verSolicitudes')

    if verSolicitudes:
        if verSolicitudes == "autorizadas":
            solicitudes = solped.objects.all().order_by('ESTADO','-OBSERVADA',).filter(ESTADO=1)

        elif verSolicitudes == "todas":
            solicitudes = solped.objects.all().order_by('ESTADO','-OBSERVADA',)

        else: 
            solicitudes = solped.objects.all().order_by('ESTADO','-OBSERVADA',).filter(ESTADO=0)

    # Aplicar los filtros si están presentes
    if fecha_desde and fecha_hasta:
        # Convertir las fechas de texto a objetos datetime
        fecha_desde = datetime.datetime.strptime(fecha_desde, '%Y-%m-%d').date()
        fecha_hasta = datetime.datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
        # Filtrar por rango de fechas
        solicitudes = solicitudes.filter(FECHA__range=(fecha_desde, fecha_hasta))

    if secretarias_seleccionados:
        #filtar por secretarias seleccionados
        solicitudes = solicitudes.filter(SECRETARIA_NOMBRE__in = secretarias_seleccionados)

    if ff_seleccionadas:
        #filtrar por ff
        solicitudes = solicitudes.filter(FUENTE_FINANCIAMIENTO__in = ff_seleccionadas)

    
    cantidad_solciitudes_pendientes = solicitudes.count()

    articulos = productoPedido.objects.all()
    total_solicitudes = solped.objects.all().count()

    total_pendientes = 0
    # Itera sobre las solicitudes pendientes y suma el resultado de TOTAL_SOLICITUD()
    for solicitud in solicitudes:
        total_pendientes += solicitud.TOTAL_SOLICITUD()
    
    # Realiza la división y formatea el resultado como sea necesario (para que aparezca la M)
    if total_pendientes > 1000000:
        total_pendientes_formatted = "{:,.2f}".format(total_pendientes / 1000000) + "M"
    else:
        total_pendientes_formatted = "{:,.2f}".format(total_pendientes)


#-- CALCULO DEL TOTAL POR SECRETARIA

    secretarias = solped.objects.filter(ESTADO=0).values_list('SECRETARIA_NOMBRE', flat=True).distinct()

    # Crear un diccionario para almacenar el total por SECRETARIA_NOMBRE
    total_por_secretaria = {}

    # Calcular el total para cada SECRETARIA_NOMBRE
    for solicitud in solicitudes:
        secretaria = solicitud.SECRETARIA_NOMBRE
        total = solicitud.TOTAL_SOLICITUD()
        total_por_secretaria.setdefault(secretaria, 0)  

        # Agregar el total al diccionario por SECRETARIA_NOMBRE
        if secretaria in secretarias:
            total_por_secretaria[secretaria] += total
        else:
            total_por_secretaria[secretaria] = total

    items = total_por_secretaria.items()

    sorted_items = sorted(items, key=lambda x: x[1])

    nombres_secretarias = [item[0] for item in sorted_items]
    totales_secretarias = [item[1] for item in sorted_items]

#-- FIN DEL CALCULO

    # Agrega esta línea para definir la cantidad de elementos por página
    items_por_pagina = 50
    paginator = Paginator(solicitudes, items_por_pagina)
    
    # Agrega el parámetro "page" para obtener la página deseada (por ejemplo, ?page=2)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'solicitudes': page, 
        'articulos':articulos,
        'total_solicitudes':total_solicitudes,
        'cantidad_solciitudes_pendientes':cantidad_solciitudes_pendientes,
        'total_pendientes':total_pendientes_formatted,
        'total_por_secretaria':total_por_secretaria,
        'nombres_secretarias': nombres_secretarias,
        'totales_secretarias': totales_secretarias,
        'page': page,
        'secretariasListado': secretariasListado,
        'fondosFinanciamiento': fondosFinanciamiento,
        }
    
    return render(request, 'solicitudes_list.html', context)

# Create your views here.
@contaduria_required
def mesa_list(request):

    solicitudes = mesa.objects.all().order_by('ESTADO',)

    solicitudes_totales = solicitudes.count()
    solicitudes_pendientes = solicitudes.filter(ESTADO=0).count()
    solicitudes_en_proceso = solicitudes.filter(ESTADO=0).count()
    solicitudes_finalizadas = solicitudes.filter(ESTADO=1).count()
    
    # Agrega esta línea para definir la cantidad de elementos por página
    items_por_pagina = 50
    paginator = Paginator(solicitudes, items_por_pagina)
    
    # Agrega el parámetro "page" para obtener la página deseada (por ejemplo, ?page=2)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'solicitudes': page, 
        'solicitudes_totales':solicitudes_totales,
        'solicitudes_pendientes':solicitudes_pendientes,
        'solicitudes_en_proceso':solicitudes_en_proceso,
        'solicitudes_finalizadas':solicitudes_finalizadas,
        'page': page,
        }
    
    return render(request, 'solicitudes-mesa.html', context)