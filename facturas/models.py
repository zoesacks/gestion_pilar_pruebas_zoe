from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from datetime import datetime
from django.utils import timezone

meses = [ 
    ("1","ENERO"),
    ("2","FEBRERO"),
    ("3","MARZO"),
    ("4","ABRIL"),
    ("5","MAYO"),
    ("6","JUNIO"),
    ("7","JULIO"),
    ("8","AGOSTO"),
    ("9","SEPTIEMBRE"),
    ("10","OCTUBRE"),
    ("11","NOVIEMBRE"),
    ("12","DICIEMBRE")
]
ejercicios = [ 
    ("2020","2020"),
    ("2021","2021"),
    ("2022","2022"),
    ("2023","2023"),
    ("2024","2024"),
    ("2025","2025")
]


# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE FONDOS
class Fondo(models.Model):
    nombre = models.CharField(max_length=120, unique=True, null=False, blank=False)
    total_fondo = models.DecimalField(max_digits=30, decimal_places=2, blank=True, null=True)

    def __str__(self):
        NAME = str(self.nombre)
        return NAME
    
    class Meta:
        verbose_name = 'Fondo'
        verbose_name_plural ='Fondos' 


# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE CODIGO FINANCIERO
class CodigoFinanciero(models.Model):
    codigo = models.CharField(max_length=20, unique=True, null=False, blank=False)
    fondo_afectado = models.ForeignKey(Fondo, on_delete=models.CASCADE, blank=True, null=True)
    nombre = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        NAME = str(self.codigo) + " - " + str(self.fondo_afectado)
        return NAME
    
    class Meta:
        verbose_name = 'Codigo'
        verbose_name_plural ='Codigos financieros' 


# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE PROYECCION DE GASTOS
class ProyeccionGastos(models.Model):
    codigo = models.ForeignKey(CodigoFinanciero, on_delete=models.CASCADE, blank=False, null = False)
    mes = models.CharField(max_length=255,null=False, blank=False, choices=meses) 
    ejercicio = models.CharField(max_length=255, null=False, blank=False, choices=ejercicios)
    importe = models.DecimalField(max_digits=30, decimal_places=2, blank=True, null=True)
    prestamo = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Proyeccion de gasto'
        verbose_name_plural ='Proyecciones de gastos' 


    def __str__(self):
        formatted_importe = '{:,.2f}'.format(self.importe)

        if self.codigo:
            NAME = str(self.codigo) + " - " + str(self.mes) + " - $" + formatted_importe
        else:
            NAME = "NO SELECCIONADO - " + str(self.mes) + " - $" + formatted_importe

        return NAME
    
    def clean(self):

        if self.importe <= 0:
             raise ValidationError("Ingrese un importe mayor a $ 0.-")
 
        super().clean()

    def save(self, *args, **kwargs):

        mes_int = int(self.mes)
        ejercicio_int = int(self.ejercicio)

        super(ProyeccionGastos, self).save(*args, **kwargs)

    def crearProyeccion(self, codigo, monto):
        proyec = ProyeccionGastos()
        proyec.codigo = codigo
        proyec.importe = monto
        proyec.ejercicio = datetime.now().year
        proyec.mes = datetime.now().month
        proyec.prestamo = True
        proyec.save()


# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE FACTURA
class Factura(models.Model):
    #CAMPOS OBLIGATORIOS
    nro_factura = models.CharField(max_length = 255, blank=True, null = True)
    proveedor = models.CharField(max_length = 255, blank=True, null = True)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True, null = True)
    codigo = models.ForeignKey(CodigoFinanciero, on_delete=models.CASCADE, blank=True, null = True)

    #CAMPOS NO OBLIGATORIOS
    emision = models.DateField(blank=True, null = True)
    alta = models.DateField(blank=True, null = True)
    oc = models.CharField(max_length = 255, blank=True, null = True)
    ff = models.CharField(max_length = 255, blank=True, null = True)
    unidad_ejecutora = models.CharField(max_length = 255, blank=True, null = True)
    objeto = models.CharField(max_length = 255, blank=True, null = True)
    fondo_afectado = models.CharField(max_length = 255, blank=True, null = True)
    ubicacion = models.CharField(max_length = 255, blank=True, null = True)

    #CAMPOS PARA MANEJO DE AUTORIZACION
    devengado = models.BooleanField(default=False)
    autorizado = models.BooleanField(default=False)
    autorizado_por = models.CharField(max_length=255, blank=True, null=True)
    autorizado_fecha = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Nro Factura: {self.nro_factura}'

    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural ='Facturas' 

    def save(self, *args, **kwargs):
        if self.existe():
            # Si ya existe una Factura con los mismos datos, no la guardes
            return
        
        else:
            self.proveedor = str(self.proveedor).strip()
            self.nro_factura = str(self.nro_factura).strip()

        super(Factura, self).save(*args, **kwargs)

    def existe(instance):
        return Factura.objects.filter(proveedor=instance.proveedor, nro_factura=instance.nro_factura).exclude(pk=instance.pk).exists()

    def autorizar(self, usuario):
        fecha = timezone.now() - timezone.timedelta(hours=3)
        self.autorizado = True
        self.autorizado_por = usuario
        self.autorizado_fecha = fecha
        self.save()


    def autorizar_automatica(self):
        self.devengado = True
        self.autorizado = True
        self.autorizado_por = "Autorizacion automatica"
        self.save()


    def desautorizar(self):
        self.autorizado = False
        self.autorizado_por = None
        self.autorizado_fecha = None
        self.save()

    @property
    def estado(self):
        ordenesPagadas = OrdenDePago.objects.filter(nro_factura=self.nro_factura, proveedor=self.proveedor, pagado = True)
        ordenesNoPagadas = OrdenDePago.objects.filter(nro_factura=self.nro_factura, proveedor=self.proveedor, pagado = False)

        if ordenesPagadas:
            subtotal = 0
            for orden in ordenesPagadas:
                subtotal += orden.total

            if subtotal == self.total:
                return "Pagada"
                    
            elif subtotal < self.total and subtotal > 0:
                return "Pagos parciales"
                    
        elif ordenesNoPagadas:
            return "OP"
                    
        else:
            if self.devengado == True:
                return "Devengado"
        
            else:
                return "Pendiente"


# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE ORDEN DE PAGO
class OrdenDePago(models.Model):
    #CAMPOS OBLIGATORIOS
    op = models.CharField(max_length=255, blank=True, null=True)
    nro_factura = models.CharField(max_length=255, blank=True, null=True)
    registro_pagado = models.CharField(max_length=255, blank=True, null=True)
    proveedor = models.CharField(max_length=255, blank=True, null=True)
    total = models.DecimalField(default=0, max_digits=25, decimal_places=2, blank=True, null=True)
    pagado = models.BooleanField(default=False)

    #OTROS CAMPOS
    fechaOp = models.DateField(blank=True, null = True)

    def __str__(self):
        return f'Orden de pago: {self.op}'

    class Meta:
        verbose_name = 'orden de pago'
        verbose_name_plural ='Ordenes de pago' 

    def save(self, *args, **kwargs):
        
        if OrdenDePago.objects.filter(proveedor=self.proveedor, nro_factura=self.nro_factura).exclude(pk=self.pk).exists():
            return
        
        self.proveedor = str(self.proveedor).strip()
        self.nro_factura = str(self.nro_factura).strip()

        try:

            facturaOp = Factura.objects.get(nro_factura=self.proveedor, proveedor=self.proveedor)

            if facturaOp.autorizado == False:
                facturaOp.autorizar_automatica()

        except ObjectDoesNotExist:
            print("La Factura no existe.")
        
        super(OrdenDePago, self).save(*args, **kwargs)


# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE CODIGO DE APROBACION
class CodigoAprobacion(models.Model):
    #CAMPOS OBLIGATORIOS
    codigo_apro = models.CharField(max_length=255, blank=True, null=True)
    monto = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True, null=True)

    def __str__(self):
        return f'Codigo de aprobacion: {self.codigo_apro}'
    
    class Meta:
        verbose_name = 'codigo de aprobacion'
        verbose_name_plural ='Codigos de aprobacion' 
        
    def save(self, *args, **kwargs):
        if CodigoAprobacion.objects.filter(codigo_apro = self.codigo_apro).exists():
            raise ValidationError("El codigo ya existe.")
        
        super(CodigoAprobacion, self).save(*args, **kwargs)
        

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE CODIGO USADO
class CodigoUsado(models.Model):
    #CAMPOS OBLIGATORIOS
    codigo = models.ForeignKey(CodigoAprobacion, on_delete=models.CASCADE, blank=True, null=True)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, blank=True, null=True)
    codigo_financiero = models.ForeignKey(CodigoFinanciero, on_delete=models.CASCADE, blank=True, null=True,default="AFECTADO")
    fecha = models.DateTimeField(blank=True, null=True)
    monto_usado = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True, null=True)
    usuario = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'Codigo usado: {self.codigo}'
    
    class Meta:
        verbose_name = 'codigo de usado'
        verbose_name_plural ='Codigos de usados' 
    

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE PRESTAMO
class Prestamo(models.Model):
    #CAMPOS OBLIGATORIOS
    codigo_entrada = models.ForeignKey(CodigoFinanciero, on_delete=models.CASCADE, blank=False, null=False, related_name="codigo_entrada")
    fecha = models.DateField(blank=False, null=False)
    codigo_salida = models.ForeignKey(CodigoFinanciero, on_delete=models.CASCADE, blank=False, null=False, related_name="codigo_salida")
    factura = models.ForeignKey(Factura, on_delete=models.PROTECT, blank=False, null=False)
    monto = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=False, null=False)

    #OTROS CAMPOS
    autorizado = models.BooleanField(default=False)
    usuario = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'Prestamo a: {self.codigo_entrada}'
    
    class Meta:
        verbose_name = 'prestamo'
        verbose_name_plural ='Prestamos' 

    def clean(self):
        if self.codigo_entrada == self.codigo_salida:
            raise ValidationError(f"El codigo financiero de destino del prestamo debe ser diferente a {self.codigo_entrada}")

        super().clean()

    @property
    def estado(self):
        devoluciones = Devolucion.objects.filter(prestamo = self)

        if devoluciones:
            subtotal = 0
            for devolucion in devoluciones:
                subtotal += devolucion.monto

            if subtotal < self.monto and subtotal > 0:
                return "Pagos parciales"
            
            else:
                return "Pagada"

        else:
            return "No pagada"



# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE DEVOLUCION
class Devolucion(models.Model):
    prestamo = models.ForeignKey(Prestamo, on_delete=models.CASCADE, blank=True, null=True)
    monto = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'Prestamo: {self.prestamo}'
    
    class Meta:
        verbose_name = 'devolucion'
        verbose_name_plural ='Devoluciones' 


