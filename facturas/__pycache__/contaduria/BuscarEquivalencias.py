from administracion.models import Equivalencia
from contaduria.models import asientosIngresos
from django.contrib import admin
from django.db.models import F

@admin.action(description="Buscar Clasificaciones")
def BuscarClasificaciones(modeladmin, request, queryset):
    # Filtrar solo los asientos sin clasificación
    asientos_sin_clasificacion = asientosIngresos.objects.filter(Clasificacion__isnull=True)

    # Obtener un diccionario de equivalencias (OrigenProgramatica: Descripcion)
    equivalencias = dict(Equivalencia.objects.values_list('OrigenProgramatica', 'Descripcion'))

    # Actualizar los asientos sin clasificación
    for asiento in asientos_sin_clasificacion:
        origen_programatica = asiento.OrigProc_Agrupamiento
        if origen_programatica in equivalencias:
            descripcion = equivalencias[origen_programatica]
            asiento.Clasificacion = Equivalencia.objects.filter(OrigenProgramatica=origen_programatica).first()
            asiento.save()
