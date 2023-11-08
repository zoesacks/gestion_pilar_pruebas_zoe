from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from administracion.models import codigoFinanciero

class Factura(models.Model):
    #CAMPOS OBLIGATORIOS
    nro_factura = models.CharField(max_length = 255, blank=True, null = False)
    proveedor = models.CharField(max_length = 255, blank=True, null = False)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True, null = False)
    codigo = models.ForeignKey(codigoFinanciero, on_delete=models.CASCADE, blank=True, null = False)

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

    def autorizar(self, usuario, fecha):
        self.autorizado = True
        self.autorizado_por = usuario
        self.autorizado_fecha = fecha
        self.save()

    def desautorizar(self):
        self.autorizado = False
        self.autorizado_por = None
        self.autorizado_fecha = None
        self.save()

    @property
    def estado(self):
        ordenesPagadas = OrdenDePago.objects.filter(nro_factura=self.nro_factura,proveedor=self.proveedor, pagado = True)
        print(f'pagadas {ordenesPagadas}')
        ordenesNoPagadas = OrdenDePago.objects.filter(nro_factura=self.nro_factura,proveedor=self.proveedor, pagado = False)
        print(f'no pagadas {ordenesNoPagadas}')  
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


class OrdenDePago(models.Model):
    #CAMPOS OBLIGATORIOS
    op = models.CharField(max_length=255, blank=True, null=False)
    nro_factura = models.CharField(max_length=255, blank=True, null=False)
    proveedor = models.CharField(max_length=255, blank=True, null=False)
    total = models.DecimalField(default=0, max_digits=25, decimal_places=2, blank=True, null=False)
    pagado = models.BooleanField(default=False)

    #OTROS CAMPOS
    fechaOp = models.DateField(blank=True, null = True)

    def __str__(self):
        return f'Orden de pago: {self.op}'

    class Meta:
        verbose_name = 'orden de pago'
        verbose_name_plural ='Ordenes de pago' 

    def save(self, *args, **kwargs):
        
        self.proveedor = str(self.proveedor).strip()
        self.nro_factura = str(self.nro_factura).strip()

        try:

            fact = str(self.nro_factura).strip()
            prove = str(self.proveedor).strip()
        
            facturaOp = Factura.objects.get(nro_factura=fact, proveedor=prove)

            usuario = "Autorizacion automatica"
            fecha = self.fechaOp
            
            facturaOp.autorizar(usuario, fecha)

        except ObjectDoesNotExist:
            print("La Factura no existe.")
        
        super(OrdenDePago, self).save(*args, **kwargs)


class CodigoAprobacion(models.Model):
    #CAMPOS OBLIGATORIOS
    codigo_apro = models.CharField(max_length=255, blank=True, null=False)
    monto = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True, null=False)

    def __str__(self):
        return f'Codigo de aprobacion: {self.codigo_apro}'
    
    class Meta:
        verbose_name = 'codigo de aprobacion'
        verbose_name_plural ='Codigos de aprobacion' 
        
    def save(self, *args, **kwargs):
        if CodigoAprobacion.objects.filter(codigo_apro = self.codigo_apro).exists():
            raise ValidationError("El codigo ya existe.")
        
        super(CodigoAprobacion, self).save(*args, **kwargs)
        

class CodigoUsado(models.Model):
    #CAMPOS OBLIGATORIOS
    codigo = models.ForeignKey(CodigoAprobacion, on_delete=models.CASCADE, blank=True, null=False)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, blank=True, null=False)
    codigo_financiero = models.ForeignKey(codigoFinanciero, on_delete=models.CASCADE, blank=True, null=False)
    fecha = models.DateTimeField(blank=True, null=False)
    monto_usado = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True, null=False)
    usuario = models.CharField(max_length=255, blank=True, null=False)

    def __str__(self):
        return f'Codigo usado: {self.codigo}'
    
    class Meta:
        verbose_name = 'codigo de usado'
        verbose_name_plural ='Codigos de usados' 
    

