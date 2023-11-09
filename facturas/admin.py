from django.contrib import admin
from django.db import models
from .models import Factura, CodigoAprobacion, CodigoUsado, OrdenDePago
from administracion.models import codigoFinanciero
from django.db.models import Sum
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields, widgets
from django.core.exceptions import ValidationError


admin.site.site_header = "Gestion Pilar"
admin.site.site_title = "Gestion Pilar"


#controlo como se importa/exporta
class facturaResource(resources.ModelResource):

        emision = fields.Field(attribute='emision',  column_name='emision')
        alta = fields.Field(attribute='alta', column_name='alta')
        codigo = fields.Field(attribute='codigo', column_name='codigo', widget=widgets.ForeignKeyWidget(codigoFinanciero, 'CODIGO')) # Acceso al campo 'codigo' en codigoFinanciero
        nro_factura = fields.Field(attribute='nro_factura', column_name='nro_factura')
        proveedor = fields.Field(attribute='proveedor', column_name='proveedor')
        oc = fields.Field(attribute='oc', column_name='oc')
        total = fields.Field(attribute='total', column_name='total')
        ff = fields.Field(attribute='ff', column_name='ff')
        unidad_ejecutora = fields.Field(attribute='unidad_ejecutora', column_name='unidad_ejecutora')
        objeto = fields.Field(attribute='objeto', column_name='objeto')
        fondo_afectado = fields.Field(attribute='fondo_afectado', column_name='fondo_afectado')
        ubicacion = fields.Field(attribute='ubicacion', column_name='ubicacion')

        devengado = fields.Field(attribute='devengado',  column_name='devengado')
        autorizado = fields.Field(attribute='autorizado',  column_name='autorizado')
        autorizado_por = fields.Field(attribute='autorizado_por',  column_name='autorizado_por')
        autorizado_fecha = fields.Field(attribute='autorizado_fecha',  column_name='autorizado_fecha')

        class Meta:
                model = Factura

        def before_import_row(self, row, **kwargs):
                # Realiza la validación antes de importar la fila
                if not row.get('codigo'):
                        raise ValidationError("El campo 'codigo' no puede estar vacío.")
                if not row.get('nro_factura'):
                        raise ValidationError("El campo 'nro de factura' no puede estar vacío.")
                if not row.get('proveedor'):
                        raise ValidationError("El campo 'proveedor' no puede estar vacío.")
                if not row.get('total'):
                        raise ValidationError("El campo 'total' no puede estar vacío.")

#controlo como se importa/exporta
class ordenDePagoResource(resources.ModelResource):
        nro_factura = fields.Field(attribute='nro_factura', column_name='nro_factura')
        proveedor = fields.Field(attribute='proveedor', column_name='proveedor')
        op = fields.Field(attribute='op', column_name='21 Nro')
        fechaOp = fields.Field(attribute='fechaOp', column_name='fecha Op')

        class Meta:
                model = OrdenDePago

@admin.register(Factura)
class FacturaAdmin(ImportExportModelAdmin):
        resource_class = facturaResource
        list_display = ('nro_factura', 'proveedor','total','estadoAdmin')
        list_filter = ('codigo', 'nro_factura', 'proveedor', 'autorizado',)

        def total_facturas(self, obj):
                importe = obj.total or 0
                return "$ {:,.2f}".format(importe)
        
        def estadoAdmin(self, obj):
                return obj.estado


@admin.register(OrdenDePago)
class OrdenDePagoAdmin(ImportExportModelAdmin):
        resource_class = ordenDePagoResource
        list_display = ('nro_factura', 'proveedor', 'op','registro_pagado','total')
        list_filter = ('nro_factura', 'proveedor', 'op')

@admin.register(CodigoAprobacion)
class CodigoAprobacionAdmin(ImportExportModelAdmin):
        list_display = ('codigo_apro', 'monto',)

@admin.register(CodigoUsado)
class CodigoUsadoAdmin(ImportExportModelAdmin):
        list_display = ('codigo', 'fecha', 'monto_usado', 'usuario',)