from django.contrib import admin
from .models import destino,configuracion,partida,destinoFondo
from import_export.admin import ImportExportModelAdmin
from .Reporte import generar_reporte


def obtener_nombre_mes(mes):
    nombres_meses = [
        "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
        "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"
    ]
    return nombres_meses[mes - 1] if 1 <= mes <= 12 else ""

@admin.register(partida)
class partidaAdmin(ImportExportModelAdmin):
    list_display = ('PARTIDA','V_F_U','tsg','tsg_correo','tsg_bomeros','tsg_justicia','tsg_fondo_educativo')
    search_fields = ('PARTIDA',)
    list_filter = ('PARTIDA','DESTINO')
    list_per_page = 30
    actions = [generar_reporte,]

    def V_F_U(self, obj):
        if obj.VALUACION_FISCAL:
            val = obj.VALUACION_FISCAL
        else:
            val = 0
        return "💲{:,.2f}".format(val)
    
    def tsg_calculada(self, obj):

        val = obj.total_tsg()
        if val >= 0:
            total = "💲{:,.2f}".format(val)
        else:
            total = "💲{:,.2f}".format(0)
        return str(total)
    
    def tsg_bruta(self, obj):

        val = obj.tsg_bruta()
        if val >= 0:
            total = "💲{:,.2f}".format(val)
        else:
            total = "💲{:,.2f}".format(0)
        return str(total)
    
    def tsg_correo(self, obj):

        val = obj.tsg_correo()
        if val >= 0:
            total = "💲{:,.2f}".format(val)
        else:
            total = "💲{:,.2f}".format(0)
        return str(total)
    
    def tsg_justicia(self, obj):

        val = obj.tsg_justicia()
        if val >= 0:
            total = "💲{:,.2f}".format(val)
        else:
            total = "💲{:,.2f}".format(0)
        return str(total)
    
    def tsg_fondo_educativo(self, obj):

        val = obj.tsg_fondo_educativo()
        if val >= 0:
            total = "💲{:,.2f}".format(val)
        else:
            total = "💲{:,.2f}".format(0)
        return total
    
    def tsg(self, obj):

        val = obj.tsg()
        if val >= 0:
            total = "💲{:,.2f}".format(val)
        else:
            total = "💲{:,.2f}".format(0)
        return str(total)
    
    def tsg_bomeros(self, obj):

        val = obj.tsg_bombero()
        if val >= 0:
            total = "💲{:,.2f}".format(val)
        else:
            total = "💲{:,.2f}".format(0)
        return str(total)
    
    def tsg_proyectada(self, obj):
        val = obj.total_tsg_proyectada()
        if val >= 0:
            total = "💲{:,.2f}".format(val)
        else:
            total = "💲{:,.2f}".format(0)
        return total


@admin.register(destinoFondo)
class destinoFondoAdmin(ImportExportModelAdmin):
    list_display = ('DESCRIPCION','MODULO',)

@admin.register(destino)
class destinoAdmin(ImportExportModelAdmin):
    list_display = ('NUM_ORDENANZA','ID_SISTEMA','DESCRIPCION','COEFICIENTE','MINIMO','EXCLUYE_FONDO','DESTINO_FONDO')

@admin.register(configuracion)
class configAdmin(ImportExportModelAdmin):
    list_display = ('periodo','ALICUOTA','MODULO','BOMBERO','CORREO','ALICUOTA_PROYECTADA')

    def periodo(self, obj):
        return f'{obj.MES}/{obj.EJERCICIO}'

