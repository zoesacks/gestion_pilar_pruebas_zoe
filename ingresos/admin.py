from django.contrib import admin
from .models import base_contribuyentes,regimen,tabla_alicuotas
from import_export.admin import ImportExportModelAdmin

# Register your models here.
@admin.register(regimen)
class regimenAdmin(ImportExportModelAdmin):
    list_display = ('NUMERO','INCISO','DESCRIPCION',)


@admin.register(tabla_alicuotas)
class tablaAlicuotasAdmin(ImportExportModelAdmin):
    list_display = ('REGIMEN','CODIGO','BASE_DESDE','BASE_HASTA','MONTO_FIJO','ALICUOTA_REAL','ALICUOTA_PROYECTADA')


@admin.register(base_contribuyentes)
class baseContribuyentesAdmin(ImportExportModelAdmin):
    list_display = ('CUENTA','base_imponible','REGIMEN','ALICUOTA_UTILIZADA','impuesto_real','ALICUOTA_PROYECTADA','impuesto_proyectado')
    list_filter = ('CUENTA','REGIMEN',)


    def ALICUOTA_UTILIZADA(self, obj):  
        formateo = obj.alicuota_utilizada()
        return formateo

    def ALICUOTA_PROYECTADA(self, obj):  
        formateo = obj.alicuota_proyectada()
        return formateo

    def base_imponible(self, obj):  
        formateo = "💲{:,.2f}".format(obj.BASE)
        return formateo
    
    def impuesto_real(self, obj):  
        formateo = "💲{:,.2f}".format(obj.impuesto())
        return formateo
    
    def impuesto_proyectado(self, obj):  
        formateo = "💲{:,.2f}".format(obj.impuesto_proyectado())
        return formateo