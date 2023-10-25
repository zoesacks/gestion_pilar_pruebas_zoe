from django.contrib import admin
from .models import partida,destino,configuracion
from import_export.admin import ImportExportModelAdmin


def obtener_nombre_mes(mes):
    nombres_meses = [
        "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
        "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"
    ]
    return nombres_meses[mes - 1] if 1 <= mes <= 12 else ""

@admin.register(partida)
class partidaAdmin(ImportExportModelAdmin):
    list_display = ('PARTIDA','V_F_U','tsg_calculada','tsg_proyectada')
    search_fields = ('PARTIDA',)
    list_filter = ('CARACTERISTICA','DESTINO')
    list_per_page = 30

    def V_F_U(self, obj):
        if obj.VALUACION_FISCAL:
            val = obj.VALUACION_FISCAL
        else:
            val = 0
        return "💲{:,.2f}".format(val)
    
    def tsg_calculada(self, obj):
        val = obj.total_tsg()
        if val >= 0:
            total = "💲{:,.2f}".format(obj.total_tsg())
        else:
            total = "💲{:,.2f}".format(0)
        return total
    
    def tsg_proyectada(self, obj):
        val = obj.total_tsg_proyectada()
        if val >= 0:
            total = "💲{:,.2f}".format(obj.total_tsg_proyectada())
        else:
            total = "💲{:,.2f}".format(0)
        return total


@admin.register(destino)
class destinoAdmin(ImportExportModelAdmin):
    list_display = ('TIPO','COEFICIENTE',)

@admin.register(configuracion)
class configAdmin(ImportExportModelAdmin):
    list_display = ('periodo','ALICUOTA','MODULO','BOMBERO','CORREO','ALICUOTA_PROYECTADA')

    def periodo(self, obj):
        return f'{obj.MES}/{obj.EJERCICIO}'

