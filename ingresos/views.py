from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from ingresos.models import base_contribuyentes,tabla_alicuotas
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_protect
from servicios_generales.models import *
from administracion.gestion_pases import ingresos_required,general_required

def sin_acceso_view(request):
    return render(request, 'sin_acceso.html', { })

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redireccionar al usuario a una página después del inicio de sesión
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required(login_url='/login/')
def home(request):

    context = {
        'lista_ventas': 'lista_ventas', 
        }
    return render(request, 'home.html', context)

@ingresos_required
def aplicaciones_ingresos(request):
    user = request.user  # Obtenemos el usuario actual
    groups = user.groups.all()  # Obtenemos los grupos a los que pertenece el usuario

    # Define una lista de aplicaciones disponibles para cada grupo
    aplicaciones_disponibles = {
        'ingresos': ['app1', 'app2', 'app3'],
    }

    aplicaciones_permitidas = []  # Inicializa la lista de aplicaciones permitidas

    # Comprueba si el usuario pertenece a algún grupo y agrega las aplicaciones permitidas
    for group in groups:
        group_name = group.name
        if group_name in aplicaciones_disponibles:
            aplicaciones_permitidas.extend(aplicaciones_disponibles[group_name])

    context = {
        'aplicaciones_permitidas': aplicaciones_permitidas,
    }

    return render(request, 'aplicaciones_ingresos.html', context)

@ingresos_required
def calculadora(request):  

    cuentas = base_contribuyentes.objects.all()

    alicuotas_lista = []
    totales_por_alicuota = []
    totales_por_alicuota_proyectada = []

    alicuotas = tabla_alicuotas.objects.values_list('ALICUOTA_REAL', flat=True).distinct()
    
    for alicuota in alicuotas:
        alicuotas_lista.append(str(f'Alic: {alicuota}'))
        
        impuesto_total = sum(cuenta.impuesto() for cuenta in cuentas if cuenta.alicuota_utilizada() == alicuota)
        totales_por_alicuota.append(float(round(impuesto_total,2)))

    alicuotas_proyectadas = tabla_alicuotas.objects.values_list('ALICUOTA_PROYECTADA', flat=True).distinct()

    for alicuota in alicuotas_proyectadas:
        impuesto_proyectado = sum(cuenta.impuesto_proyectado() for cuenta in cuentas if cuenta.alicuota_proyectada() == alicuota)
        totales_por_alicuota_proyectada.append(float(round(impuesto_proyectado,2)))


    alicuotas_lista.reverse()
    totales_por_alicuota.reverse()
    totales_por_alicuota_proyectada.reverse()


    datos_grafico = []
    
    for i, alicuota in enumerate(alicuotas_lista):
        total = totales_por_alicuota[i]
        total_proyectado = totales_por_alicuota_proyectada[i]
        datos_grafico.append((alicuota, total, total_proyectado))


    #calculo de tarjetas
    total_impuesto_real = sum(cuenta.impuesto() for cuenta in cuentas)
    total_impuesto_proyectado = sum(cuenta.impuesto_proyectado() for cuenta in cuentas)
    diferencia = total_impuesto_proyectado - total_impuesto_real

    items_por_pagina = 20
    paginator = Paginator(cuentas, items_por_pagina)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'page':page, 
        'total_impuesto_real':total_impuesto_real,

        'datos_grafico':datos_grafico,

        'alicuotas':alicuotas_lista,
        'totales_por_alicuota':totales_por_alicuota,

        'totales_por_alicuota_proyectada':totales_por_alicuota_proyectada,
        
        'total_impuesto_proyectado':total_impuesto_proyectado, 
        'diferencia':diferencia,
        }
    
    return render(request, 'calculadora.html', context)

@ingresos_required
def serivicios_generales(request):  

    partidas = partida.objects.all()

    total_tasas = partida.objects.all().count()

    total_proyectado = 0

    total_emision = 0

    items_por_pagina = 20
    paginator = Paginator(partidas, items_por_pagina)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'page':page, 
        'total_tasas':total_tasas,
        'total_emision':total_emision,
        'total_proyectado':total_proyectado,
        }
    
    return render(request, 'serivicios_generales.html', context)
