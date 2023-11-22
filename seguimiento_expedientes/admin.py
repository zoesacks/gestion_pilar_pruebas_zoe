from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .models import Sector, Usuario, TipoDocumento, Documento, Transferencia


@admin.register(Sector)
class SectorAdmin(ImportExportModelAdmin):
    list_display = ('nombre',)

@admin.register(Usuario)
class UsuarioAdmin(ImportExportModelAdmin):
    list_display = ('sector', 'usuario')

@admin.register(TipoDocumento)
class TipoDocumentoAdmin(ImportExportModelAdmin):
    list_display = ('numero', 'descripcion',)
    
@admin.register(Documento)
class DocumentoAdmin(ImportExportModelAdmin):
    list_display = ('tipo', 'numero', 'ejercicio', 'sector', 'propietario')
    readonly_fields = ('sector',)
    
@admin.register(Transferencia)
class TransferenciaAdmin(ImportExportModelAdmin):
    list_display = ('documento', 'estado', 'fecha', 'emisor', 'receptor')
    readonly_fields = ('emisor', 'fecha_confirmacion', 'recepcion_confirmada', 'fecha')
    
    actions = ['confirmarRecepcion']

    def estado(self, obj):
        return obj.estado
    
    @admin.action(description= "Confirmar recepcion")
    def confirmarRecepcion(self, obj, queryset):
        for obj in queryset:
            obj.confirmarRecepcion()
    
