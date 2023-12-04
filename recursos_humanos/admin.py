from django.contrib import admin


from import_export.admin import ImportExportModelAdmin
from .models import DatosPersonales, Legajo, Domicilio, Estudio, Familiar, Licencia, UsoLicencia
from .models import Cargo, Categoria, Escolariodad, EstodoCivil, Localidad, Nacionalidad, Oficina, Particion, Provincia, Relacion, TipoLicencia, TipoEstudio, TipoDeDocumento, Feriado

# Register your models here.

class DatosPersonalesInline(admin.StackedInline):
    model = DatosPersonales
    min_num = 1 
    max_num = 1

class DomicilioInline(admin.StackedInline):
    model = Domicilio
    min_num = 1 
    extra = 0

class EstudioInline(admin.StackedInline):
    model = Estudio
    extra = 0

class FamiliarInline(admin.StackedInline):
    model = Familiar
    extra = 0

class LicenciaInline(admin.StackedInline):
    model = Licencia
    extra = 0

class UsoLicenciaInline(admin.StackedInline):
    model = UsoLicencia
    extra = 0

@admin.register(Legajo)
class LegajoAdmin(ImportExportModelAdmin):
    list_display = ('num_legajo', 'nombre', 'oficina' )
    inlines = [
        DatosPersonalesInline,
        DomicilioInline,
        LicenciaInline,
        FamiliarInline,
        EstudioInline,
    ]

    def nombre(self, obj):
        return DatosPersonales.objects.get(legajo = obj)

@admin.register(DatosPersonales)
class DatosPersonalesAdmin(ImportExportModelAdmin):
    list_display = ('legajo', 'tipo_doc', 'num_doc', 'nombre', 'apellido',)

@admin.register(Domicilio)
class DomicilioAdmin(ImportExportModelAdmin):
    list_display = ('legajo', 'provincia', 'localidad', 'calle', 'altura',)

@admin.register(Estudio)
class EstudioAdmin(ImportExportModelAdmin):
    list_display = ('legajo', 'tipo_estudio', 'inicio', 'fin', 'completo',)

@admin.register(Familiar)
class FamiliarAdmin(ImportExportModelAdmin):
    list_display = ('legajo', 'relacion', 'tipo_doc', 'num_doc', 'apellido', 'nombre',)

@admin.register(Licencia)
class LicenciaAdmin(ImportExportModelAdmin):
    list_display = ('legajo', 'dias', 'tipo_licencia', 'dias_habiles', 'dias_pendientes',)
    inlines = [
        UsoLicenciaInline,
    ]

    

    
@admin.register(UsoLicencia)
class UsoLicenciaAdmin(ImportExportModelAdmin):
    list_display = ('licencia', 'fecha_inicio', 'fecha_fin',)



@admin.register(Cargo)
class CargoAdmin(ImportExportModelAdmin):
    list_display = ('numero', 'descripcion',)

@admin.register(Categoria)
class CategoriaAdmin(ImportExportModelAdmin):
    list_display = ('numero', 'descripcion',)

@admin.register(Escolariodad)
class EscolariodadAdmin(ImportExportModelAdmin):
    list_display = ('numero', 'descripcion',)

@admin.register(EstodoCivil)
class EstodoCivilAdmin(ImportExportModelAdmin):
    list_display = ('numero', 'descripcion',)

@admin.register(Localidad)
class LocalidadAdmin(ImportExportModelAdmin):
    list_display = ('numero', 'descripcion',)

@admin.register(Nacionalidad)
class NacionalidadAdmin(ImportExportModelAdmin):
    list_display = ('numero', 'descripcion',)

@admin.register(Oficina)
class OficinaAdmin(ImportExportModelAdmin):
    list_display = ('numero', 'descripcion',)

@admin.register(Particion)
class ParticionAdmin(ImportExportModelAdmin):
    list_display = ('numero', 'descripcion',)

@admin.register(Provincia)
class ProvinciaAdmin(ImportExportModelAdmin):
    list_display = ('numero', 'descripcion',)

@admin.register(Relacion)
class RelacionAdmin(ImportExportModelAdmin):
    list_display = ('numero', 'descripcion',)

@admin.register(TipoLicencia)
class TipoLicenciaAdmin(ImportExportModelAdmin):
    list_display = ('descripcion',)

@admin.register(TipoEstudio)
class TipoEstudioAdmin(ImportExportModelAdmin):
    list_display = ('numero', 'descripcion',)

@admin.register(TipoDeDocumento)
class TipoDeDocumentoAdmin(ImportExportModelAdmin):
    list_display = ('numero', 'descripcion',)


@admin.register(Feriado)
class FechaAdmin(ImportExportModelAdmin):
    list_display = ('fecha', 'descripcion',)