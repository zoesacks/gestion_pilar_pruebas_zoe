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
    list_display = ('tipo', 'numero', 'ejercicio', 'propietario',)
    readonly_fields = ('fecha_alta', 'en_transito', 'destinatario', 'fecha_transito', 'observacion', 'transferencias')
    
@admin.register(Transferencia)
class TransferenciaAdmin(ImportExportModelAdmin):
    list_display = ('fecha', 'emisor', 'receptor', 'fecha_confirmacion',)
    readonly_fields = ('fecha', 'emisor', 'receptor', 'fecha_confirmacion',)
    
    
