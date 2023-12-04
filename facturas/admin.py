import datetime
from django.contrib import admin
from django.db import models
from .models import Factura, CodigoAprobacion, CodigoUsado, OrdenDePago, CodigoFinanciero, Fondo, ProyeccionGastos, Prestamo, Devolucion
from django.db.models import Sum
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields, widgets
from django.core.exceptions import ValidationError
from django.db.models.functions import ExtractMonth
from django.utils import timezone


admin.site.site_header = "Regresar a la App"
admin.site.site_title = "Regresar a la App"


#controlo como se importa/exporta
class FacturaResource(resources.ModelResource):

        emision = fields.Field(attribute='emision',  column_name='emision')
        alta = fields.Field(attribute='alta', column_name='alta')
        codigo = fields.Field(attribute='codigo', column_name='codigo', widget=widgets.ForeignKeyWidget(CodigoFinanciero, 'codigo')) # Acceso al campo 'codigo' en codigoFinanciero
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
                
class FacturaExportResource(FacturaResource):
    estado = fields.Field(column_name='estado', attribute='estado')

    def dehydrate(self, row):
        # Agrega el campo 'estado' al resultado final durante la exportación
        row['estado'] = row.instance.estado
        return row

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
        resource_class = FacturaResource
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

@admin.register(Fondo)
class FondoAdmin(ImportExportModelAdmin):
    list_display = ('nombre',)
    list_filter = ('nombre',)

@admin.register(CodigoFinanciero)
class CodigoFinancieroAdmin(ImportExportModelAdmin):
    list_display = ('codigo',)
    list_filter = ('codigo',)

@admin.register(ProyeccionGastos)
class ProyeccionGastosAdmin(ImportExportModelAdmin):
    list_display = ('codigo', 'periodo', 'total_proyectado',)
    list_filter = ('codigo',  'mes', 'ejercicio')

    def total_proyectado(self, obj):
        return "💲{:,.2f}".format(obj.importe)
    
    def periodo(self, obj):
        msj = f'{obj.mes} - {obj.ejercicio}'
        return msj


def proyeccionDeGastos(obj, codigo):
        #obtengo el dinero disponible del mes
        proyeccionesSalida = ProyeccionGastos.objects.filter(codigo = codigo, mes = obj.fecha.month, ejercicio = obj.fecha.year)
        totalDisponible = proyeccionesSalida.aggregate(total=Sum('importe'))['total'] or 0

        #obtengo el dinero total de las facturas autorizadas del mes
        facturasAutorizadas = Factura.objects.filter(codigo__codigo= codigo, autorizado_fecha__month = ExtractMonth(timezone.now()))
        totalFacturasAutorizadas = facturasAutorizadas.aggregate(total=Sum('total'))['total'] or 0

        totalDisponible = float(round(totalDisponible - totalFacturasAutorizadas, 2))

        return totalDisponible
     
@admin.register(Prestamo)
class PestamoAdmin(ImportExportModelAdmin):
    list_display = ('fecha', 'codigo_entrada', 'codigo_salida', 'factura', 'monto', 'autorizado', 'estado')
    list_filter = ('fecha', 'codigo_entrada', 'codigo_salida', 'factura')
    readonly_fields = ('autorizado', )

    actions = ['autorizar_prestamo']

    def pagado(self, obj):
        return obj.estado()
    
    @admin.action(description= "Autorizar Prestamo")
    def autorizar_prestamo(self, obj, queryset):

        for obj in queryset:

                totalDisponibleCodSalida = proyeccionDeGastos(obj, obj.codigo_salida)
                totalDisponibleCodEntrada = proyeccionDeGastos(obj, obj.codigo_entrada)

                if obj.factura.devengado == True and obj.factura.autorizado == False:

                        if obj.monto <= totalDisponibleCodSalida and obj.factura.total <= totalDisponibleCodSalida + totalDisponibleCodEntrada:

                                ProyeccionGastos().crearProyeccion(obj.codigo_salida, -obj.monto)
                                ProyeccionGastos().crearProyeccion(obj.codigo_entrada, obj.monto)

                                usuario = "Autorizacion por prestamo"
                                obj.factura.autorizar(usuario)

                                obj.autorizado = True
                                obj.save()
                        
                        else:
                                print("s" + str(totalDisponibleCodSalida))
                                print(totalDisponibleCodEntrada)
                                raise ValidationError("El codigo no tiene dinero suficiente")
                
                else:
                       raise ValidationError("La factura debe estar devengada y pendiente de autorizacion")
                       




@admin.register(Devolucion)
class DevolucionAdmin(ImportExportModelAdmin):
    list_display = ('fecha', 'prestamo', 'monto',)
    list_filter = ('fecha', 'prestamo', 'monto',)



        
      
       

       



