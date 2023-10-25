from django.shortcuts import render
from administracion.gestion_pases import tesoreria_required
# Create your views here.

@tesoreria_required
def aplicaciones_tesoreria(request):

    context = {
        'lista_ventas': 'lista_ventas', 
        }
    return render(request, 'aplicaciones_tesoreria.html', context)

