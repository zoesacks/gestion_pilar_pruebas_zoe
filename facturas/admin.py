from django.contrib import admin
from django.db import models
from .models import factura, codigoAprobacion, codigoUsado, ordenDePago
from administracion.models import codigoFinanciero
from django.db.models import Sum
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields, widgets
from django.core.exceptions import ValidationError


admin.site.site_header = "Gestion Pilar"
admin.site.site_title = "Gestion Pilar"


#controlo como se importa/exporta
class facturaResource(resources.ModelResource):
        autorizado_por = fields.Field(attribute='autorizado_por',  column_name='autorizado_por')
        autorizado_fecha = fields.Field(attribute='autorizado_fecha',  column_name='autorizado_fecha')
        emision = fields.Field(attribute='emision',  column_name='emision')
        alta = fields.Field(attribute='alta', column_name='alta')
        codigo = fields.Field(attribute='codigo', column_name='codigo', widget=widgets.ForeignKeyWidget(codigoFinanciero, 'CODIGO')) # Acceso al campo 'codigo' en codigoFinanciero
        nroFactura = fields.Field(attribute='nroFactura', column_name='nroFactura')
        proveedor = fields.Field(attribute='proveedor', column_name='proveedor')
        oc = fields.Field(attribute='oc', column_name='oc')
        total = fields.Field(attribute='total', column_name='total')
        ff = fields.Field(attribute='ff', column_name='ff')
        unidadEjecutora = fields.Field(attribute='unidadEjecutora', column_name='unidadEjecutora')
        objeto = fields.Field(attribute='objeto', column_name='objeto')
        fondoAfectado = fields.Field(attribute='fondoAfectado', column_name='fondoAfectado')

        class Meta:
                model = factura

        def before_import_row(self, row, **kwargs):
                # Realiza la validación antes de importar la fila
                if not row.get('codigo'):
                        raise ValidationError("El campo 'codigo' no puede estar vacío.")
                if not row.get('nroFactura'):
                        raise ValidationError("El campo 'nro de factura' no puede estar vacío.")
                if not row.get('proveedor'):
                        raise ValidationError("El campo 'proveedor' no puede estar vacío.")
                if not row.get('total'):
                        raise ValidationError("El campo 'total' no puede estar vacío.")


#controlo como se importa/exporta
class ordenDePagoResource(resources.ModelResource):
        nroFactura = fields.Field(attribute='nroFactura', column_name='nroFactura')
        proveedor = fields.Field(attribute='proveedor', column_name='proveedor')
        op = fields.Field(attribute='op', column_name='21 Nro')
        fechaOp = fields.Field(attribute='fechaOp', column_name='fecha Op')

        class Meta:
                model = ordenDePago


@admin.register(factura)
class facturaAdmin(ImportExportModelAdmin):
        resource_class = facturaResource
        list_display = ('nroFactura', 'proveedor', 'total_facturas',)
        list_filter = ('estado', 'codigo', 'nroFactura', 'proveedor',)
        exclude = ('estado',)

        def total_facturas(self, obj):
                importe = obj.total or 0
                return "$ {:,.2f}".format(importe)
        

@admin.register(ordenDePago)
class ordenDePagoAdmin(ImportExportModelAdmin):
        resource_class = ordenDePagoResource
        list_display = ('nroFactura', 'proveedor', 'op')
        list_filter = ('nroFactura', 'proveedor', 'op')


@admin.register(codigoAprobacion)
class codigoAprobacionAdmin(ImportExportModelAdmin):
        list_display = ('codigoApro', 'monto',)

@admin.register(codigoUsado)
class codigoUsadoAdmin(ImportExportModelAdmin):
        list_display = ('codigo', 'fecha', 'montoUsado', 'usuario',)