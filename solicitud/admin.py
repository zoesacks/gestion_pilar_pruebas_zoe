from django.contrib import admin

# Register your models here.
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from solicitud.Autorizar import autorizarSolped,cancelarSolped
from solicitud.models import *


@admin.register(productoPedido)
class productoPedidoAdmin(ImportExportModelAdmin):
    list_display = ('pedido','articulo','cantidad','objeto')

@admin.register(mesa)
class mesaAdmin(ImportExportModelAdmin):
    list_display = ('FECHA','TITULO','USUARIO','DESARROLLADOR','ESTADO')


class productoPedidoInline(admin.TabularInline):
    model = productoPedido
    extra = 1
    fields = ('articulo', 'cantidad','objeto','precio_unitario','total')

@admin.register(solped)
class solpedAdmin(ImportExportModelAdmin):
    #resource_class = solpedResource  # Asignar la clase solpedResource a este modelo

    inlines = [
        productoPedidoInline,
    ]
        
    list_display = ('solicitud','DETALLE','total','comentarios','estado')
    list_display_links = ('solicitud',)
    exclude = ('ESTADO','ARTICULO','TOTAL','AUTORIZADO_POR','FECHA_AUTORIZADO','OBSERVADA')
    search_fields =('DETALLE',)
    list_filter = ('FECHA','NUMERO','ESTADO','SECRETARIA',)
    
    actions = [autorizarSolped,cancelarSolped]

    def comentarios(self,obj):
        return obj.COMENTARIOS


    #def fecha(self,obj):
    #    return obj.FECHA.strftime('%d/%m/%Y')

    def total(self, obj):
        return "💲{:,.2f}".format(obj.TOTAL_SOLICITUD())
    
    def solicitud(self,obj):
        return f'{obj.CODIGO}'
    
    def estado(self, obj):

        return "🔴 Pendiente" if obj.ESTADO == 0 else f"Autorizado por: {obj.AUTORIZADO_POR} el {obj.FECHA_AUTORIZADO}" #.strftime('%d/%m/%Y %H:%M')
