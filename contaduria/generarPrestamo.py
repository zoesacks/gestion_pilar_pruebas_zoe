
from datetime import date
from contaduria.models import prestamo,regularizacion
from django.contrib import admin
from django.contrib import messages


@admin.action(description="Generar Prestamo")
def generarPrestamo(modeladmin, request, queryset):
    if queryset.count() == 1:
        obj = queryset.first()
        if obj.FuenteFinanciamiento != "1.1.0 - TESORO MUNICIPAL":
            if obj.Pagado > 0:
                nuevo_prestamo = prestamo(
                    FECHA=date.today(),
                    GASTO=obj,
                    IMPORTE=obj.Pagado,
                    PENDIENTE=-obj.Pagado,
                    REGISTRO_PAGADO=f'{obj.AplicacionTipo} - {obj.AplicacionEjercicio} - {obj.AplicacionNumero}',
                    PROVEEDOR=f'{obj.ProveedorTipo} - {obj.ProveedorNumero} - {obj.RazonSocial}'
                )
                nuevo_prestamo.save()
            else:
                messages.warning(request, "El importe Pagado es menor o igual a $ 0.-")
        
        else:
            messages.warning(request, "La fuente de financiamiento del gasto seleccionado no corresponde a '1.1.0 - Tesoro municipal', por favor seleccione otro gasto.")
    else:
        messages.warning(request, "Solo se puede generar un prestamo a la vez. Por favor seleccione 1 solo registro.")





@admin.action(description="Generar Regularizacion")
def generarRegularizacion(modeladmin, request, queryset):
    
    if queryset.count() == 1:

        obj = queryset.first()

        if obj.FuenteFinanciamiento == "1.1.0":
            if obj.Pagado < 0:
                nueva_regularizacion = regularizacion(
                    FECHA=date.today(),
                    GASTO=obj,
                    IMPORTE=obj.Pagado,
                    REGISTRO_PAGADO=f'{obj.AplicacionTipo} - {obj.AplicacionEjercicio} - {obj.AplicacionNumero}',
                    PROVEEDOR=f'{obj.ProveedorTipo} - {obj.ProveedorNumero} - {obj.RazonSocial}'
                )
                nueva_regularizacion.save()
            else:
                messages.warning(request, "El importe Pagado es mayor o igual a $ 0.- las regularizaciones de los gastos deben ser negativas.")
        
        else:
            messages.warning(request, "La fuente de financiamiento del gasto seleccionado no corresponde a '1.1.0 - Tesoro municipal', por favor seleccione otro gasto.")
    else:
        messages.warning(request, "Solo se puede generar una regularizacion a la vez. Por favor seleccione 1 solo registro del pagado.")