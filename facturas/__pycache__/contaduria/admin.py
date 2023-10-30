from django import forms
from django.contrib import admin
from contaduria.models import *

import calendar
from django.db.models.functions import ExtractMonth
from import_export.admin import ImportExportModelAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import SimpleListFilter
from django.db.models import Sum
from contaduria.generarPrestamo import generarPrestamo,generarRegularizacion
from contaduria.forms import ProyeccionGastosForm,ProyeccionIngresosForm
from contaduria.BuscarEquivalencias import BuscarClasificaciones

class MonthFilter(admin.SimpleListFilter):
    title = _('Mes')
    parameter_name = 'month'

    def lookups(self, request, model_admin):
        months = model_admin.model.objects.annotate(month=ExtractMonth('Fecha')).order_by('month').values_list('month', flat=True).distinct()
        return [(month, _(calendar.month_name[month])) for month in months]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(Fecha__month=self.value())

class ProveedorFilter(SimpleListFilter):
    title = _('Proveedor')
    parameter_name = 'proveedor'

    def lookups(self, request, model_admin):
        # Obtener los proveedores únicos de la base de datos
        proveedores = model_admin.get_queryset(request).values_list('ProveedorTipo', 'ProveedorNumero', 'RazonSocial').distinct()
        # Generar las opciones del filtro
        return tuple((f'{tipo} - {numero} - {razon_social}', f'{tipo} - {numero} - {razon_social}') for tipo, numero, razon_social in proveedores)

    def queryset(self, request, queryset):
        # Aplicar el filtro según la opción seleccionada
        if self.value():
            tipo, numero, razon_social = self.value().split(' - ')
            return queryset.filter(ProveedorTipo=tipo, ProveedorNumero=numero, RazonSocial=razon_social)

@admin.register(asientosGastos)
class asientosGastosAdmin(ImportExportModelAdmin):
    list_display=('Ejercicio','Fecha','jurisdiccion','fuente_financiamiento','estructura_programatica','objeto_del_gasto','comprobante','aplicacion','PAGADO',)
    list_filter = (MonthFilter,'RazonSocial','AplicacionNumero','ComprobanteTipo')

    ordering=('Pagado',)
    list_per_page=50
    actions = [generarPrestamo,generarRegularizacion]
    def jurisdiccion(self, obj):
        if obj.Jurisdiccion:
            name = f'{obj.Jurisdiccion} - {obj.JurisdiccionDescripcion}'
        else:
            name = ""
        return name 
     
    def estructura_programatica(self, obj):
        if obj.EstructuraProgramatica:
            name = f'{obj.EstructuraProgramatica} - {obj.EstructuraProgramaticaDescripcion}'
        else:
            name = ""
        return name 
    
    def fuente_financiamiento(self, obj):
        if obj.FuenteFinanciamiento:
            name = f'{obj.FuenteFinanciamiento} - {obj.FuenteFinanciamientoDescripcion}'
        else:
            name = ""
        return name 
    
    def objeto_del_gasto(self, obj):
        if obj.ObjetodelGasto:
            name = f'{obj.ObjetodelGasto} - {obj.ObjetodelGastoDescripcion}'
        else:
            name = ""
        return name 
    
    def comprobante(self, obj):
        if obj.ComprobanteTipo:
            name = f'{obj.ComprobanteTipo} - {obj.ComprobanteEjercicio} - {obj.ComprobanteNumero}'
        else:
            name = ""
        return name 
    
    def aplicacion(self, obj):
        if obj.AplicacionTipo:
            name = f'{obj.AplicacionTipo} - {obj.AplicacionEjercicio} - {obj.AplicacionNumero}'
        else:
            name = ""
        return name 

    def proveedor(self, obj):
        if obj.ProveedorTipo:
            name = f'{obj.ProveedorTipo} - {obj.ProveedorNumero} - {obj.RazonSocial}'
        else:
            name = ""
        return name 

    def PAGADO(self, obj):
        return "💲{:,.2f}".format(obj.Pagado)
    
@admin.register(asientosIngresos)
class asientosIngresosAdmin(ImportExportModelAdmin):
    list_display=('Ejercicio','Fecha','Clasificacion','Recurso_Descripcion','OrigProc_Descripcion','DEVENGADO','PERCIBIDO',)
    list_filter = ('Clasificacion','Recurso_Descripcion','OrigProc_Descripcion','Fecha')
    ordering=('-Fecha',)
    list_per_page=50
    exclude = ('Ejercicio',)
    actions = [BuscarClasificaciones]

    def DEVENGADO(self, obj):
        return "💲{:,.2f}".format(obj.Devengado)
    
    def PERCIBIDO(self, obj):
        return "💲{:,.2f}".format(obj.Percibido)

class PendienteZeroFilter(admin.SimpleListFilter):
    title = _('Todos los Prestamos')
    parameter_name = 'pendiente_zero'

    def lookups(self, request, model_admin):
        return (
            ('yes', _('Prestamos Cancelados')),
            ('no', _('Prestamos Pendientes')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(PENDIENTE=0)
        if self.value() == 'no':
            return queryset.exclude(PENDIENTE=0)

@admin.register(prestamo)
class prestamoAdmin(ImportExportModelAdmin):
    list_display=('GASTO','FECHA','FONDO','total','pendiente_devolucion','ORDEN_DE_PAGO','REGISTRO_PAGADO','PROVEEDOR',)
    exclude =('GASTO',)
    list_filter = (PendienteZeroFilter,)
    
    def total(self, obj):
        return "💲{:,.2f}".format(obj.IMPORTE)
        
    def pendiente_devolucion(self, obj):
        return "💲{:,.2f}".format(obj.PENDIENTE)
    
    def proveedor(self, obj):
        MSJ = F'{obj.GASTO.PROVEEDO}'
        return MSJ
   
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        
        return queryset
    
    def changelist_view(self, request, extra_context=None):
        # Agregar el total al contexto de la vista
        extra_context = extra_context or {}

        # Obtener el total de los importes
        total_importes = self.get_queryset(request).aggregate(total=Sum('IMPORTE'))['total']

        # Agregar el total al contexto
        extra_context['total_importes'] = total_importes
        
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(devolucionPrestamo)
class devolucionPrestamoAdmin(ImportExportModelAdmin):
    list_display=('PRESTAMO','FECHA','total','FONDO','ORDEN_DE_PAGO','REGISTRO_PAGADO','PROVEEDOR',)
    exclude =('PENDIENTE','FONDO','ORDEN_DE_PAGO','REGISTRO_PAGADO','PROVEEDOR')
    list_filter = ('PRESTAMO',)
    def total(self, obj):
        return "💲{:,.2f}".format(obj.IMPORTE)

class ProyeccionGastosForm(forms.ModelForm):
    class Meta:
        model = proyeccionGastos
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProyeccionGastosForm, self).__init__(*args, **kwargs)
        # Filtrar los proveedores disponibles en el queryset del campo 'PROVEEDOR'
        self.fields['PROVEEDOR'].queryset = proveedor.objects.all()

class ProyeccionIngresosForm(forms.ModelForm):
    class Meta:
        model = proyeccionIngresos
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProyeccionIngresosForm, self).__init__(*args, **kwargs)
        # Filtrar los proveedores disponibles en el queryset del campo 'PROVEEDOR'
        self.fields['RECURSO'].queryset = recurso.objects.all()

@admin.register(proyeccionGastos)
class proyeccionGastosAdmin(ImportExportModelAdmin):
    form = ProyeccionGastosForm
    list_display = ('CODIGO', 'PROVEEDOR', 'CONCEPTO', 'periodo', 'total_proyectado',)
    exclude = ('MODIFICADO_POR', 'FECHA_MODIFICACION', 'PERIODO')
    ordering = ('PERIODO',)
    list_filter = ('CODIGO', 'PROVEEDOR', 'CONCEPTO', 'MES', 'EJERCICIO')

    def total_proyectado(self, obj):
        return "💲{:,.2f}".format(obj.IMPORTE)
    
    def periodo(self, obj):
        msj = f'{obj.MES} - {obj.EJERCICIO}'
        return msj

@admin.register(proyeccionIngresos)
class proyeccionIngresosAdmin(ImportExportModelAdmin):
    form = ProyeccionIngresosForm
    list_display = ('RECURSO', 'CLASIFICACION','periodo', 'total_proyectado',)
    exclude = ('MODIFICADO_POR', 'FECHA_MODIFICACION', 'PERIODO')
    ordering = ('PERIODO',)
    list_filter = ('RECURSO','MES','EJERCICIO')

    def total_proyectado(self, obj):
        return "💲{:,.2f}".format(obj.IMPORTE)
    
    def periodo(self, obj):
        msj = f'{obj.MES} - {obj.EJERCICIO}'
        return msj

@admin.register(regularizacion)
class regularizacionAdmin(ImportExportModelAdmin):
    list_display=('GASTO','FECHA','FONDO','total','REGISTRO_PAGADO','PROVEEDOR',)
    exclude =('GASTO',)    
    
    def total(self, obj):
        return "💲{:,.2f}".format(obj.IMPORTE)
