from django.contrib import admin
from administracion.models import fondo,proveedor,concepto,Equivalencia,recurso,codigoFinanciero,desarrollador
from import_export.admin import ImportExportModelAdmin

@admin.register(concepto)
class conceptoAdmin(ImportExportModelAdmin):
    list_display = ('NOMBRE',)
    list_filter = ('NOMBRE',)

@admin.register(Equivalencia)
class EquivalenciaAdmin(ImportExportModelAdmin):
    list_display=('OrigenProgramatica','Descripcion') 

@admin.register(fondo)
class fondoAdmin(ImportExportModelAdmin):
    list_display = ('CODIGO', 'NOMBRE',)
    list_filter = ('CODIGO', 'NOMBRE',)
    
@admin.register(recurso)
class recursoAdmin(ImportExportModelAdmin):
    list_display = ('CODIGO', 'NOMBRE',)
    list_filter = ('CODIGO', 'NOMBRE',)

@admin.register(proveedor)
class proveedorAdmin(ImportExportModelAdmin):
    list_display = ('CODIGO', 'TIPO','RAZON_SOCIAL', 'ESTADO',)
    list_filter = ('CODIGO', 'TIPO','RAZON_SOCIAL', 'ESTADO',)
    
    def estado(self, obj):
        if obj.ESTADO == 0:
            return "🔴 Inactivo"
        else:
            return "🟢 Activo"

@admin.register(codigoFinanciero)
class recursoAdmin(ImportExportModelAdmin):
    list_display = ('CODIGO', 'NOMBRE',)
    list_filter = ('CODIGO', 'NOMBRE',)

@admin.register(desarrollador)
class desarrolladorAdmin(ImportExportModelAdmin):
    list_display = ('LEGAJO', 'NOMBRE',)
    list_filter = ('LEGAJO', 'NOMBRE',)