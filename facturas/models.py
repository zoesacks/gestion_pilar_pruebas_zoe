from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from administracion.models import codigoFinanciero

class factura(models.Model):
    estado_choice = (
        ('Pendiente', 'Pendiente'),
        ('Autorizado', 'Autorizado'),
        ('OP', 'OP'),
    )

    autorizado_por = models.CharField(max_length=255, blank=True, null=True)
    autorizado_fecha = models.DateTimeField(blank=True, null=True)
    emision = models.DateField(blank=True, null = True)
    alta = models.DateField(blank=True, null = True)
    codigo = models.ForeignKey(codigoFinanciero, on_delete=models.CASCADE, blank=True, null=True)
    nroFactura = models.CharField(max_length = 255, blank=True, null = True)
    proveedor = models.CharField(max_length = 255, blank=True, null = True)
    oc = models.CharField(max_length = 255, blank=True, null = True)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True, null = True )
    ff = models.CharField(max_length = 255, blank=True, null = True)
    unidadEjecutora = models.CharField(max_length = 255, blank=True, null = True)
    objeto = models.CharField(max_length = 255, blank=True, null = True)
    fondoAfectado = models.CharField(max_length = 255, blank=True, null = True)
    estado = models.CharField(max_length=20, choices=estado_choice, default='Pendiente')

    def __str__(self):
        return f'Nro factura: {self.nroFactura}'

    class Meta:
        verbose_name = 'factura'
        verbose_name_plural ='Facturas' 

    def clean(self):

        if not self.codigo:  
            raise ValidationError("El campo codigo no puede estar vacío.")

        if not self.nroFactura:
            raise ValidationError("El campo nro de factura no puede estar vacío.")
                          
        if not self.proveedor:
            raise ValidationError("El campo proveedor no puede estar vacío.")

        if not self.total:
            raise ValidationError("El campo total no puede estar vacío.")

        super().clean()


    def save(self, *args, **kwargs):
        if self.existe():
            # Si ya existe una factura con los mismos datos, no la guardes
            return
        else:
            self.proveedor = str(self.proveedor).strip()
            self.nroFactura = str(self.nroFactura).strip()

        super(factura, self).save(*args, **kwargs)

    def existe(instance):
        return factura.objects.filter(proveedor=instance.proveedor, nroFactura=instance.nroFactura).exclude(pk=instance.pk).exists()


class ordenDePago(models.Model):
    op = models.CharField(max_length = 255, blank=True, null = True)
    fechaOp = models.DateField(blank=True, null = True)
    nroFactura = models.CharField(max_length = 255, blank=True, null = True)
    proveedor = models.CharField(max_length = 255, blank=True, null = True)

    def save(self, *args, **kwargs):
        
        self.proveedor = str(self.proveedor).strip()
        self.nroFactura = str(self.nroFactura).strip()

        try:
            #print(f'Filtrando proveedor: {self.proveedor} factura {self.nroFactura}')

            fact = str(self.nroFactura).strip()
            prove = str(self.proveedor).strip()
        
            facturaOp = factura.objects.get(nroFactura=fact, proveedor=prove)


            if facturaOp.estado in ['Pendiente', 'Autorizado']:
                
                facturaOp.estado = 'OP'
                facturaOp.autorizado_fecha = self.fechaOp
                #facturaOp.auto
                facturaOp.save()

        except ObjectDoesNotExist:
            # La factura no existe, puedes manejarlo de acuerdo a tus necesidades
            # Por ejemplo, imprimir un mensaje de registro
            print("La factura no existe.")
        

        super(ordenDePago, self).save(*args, **kwargs)

class codigoAprobacion(models.Model):
    codigoApro = models.CharField(max_length=255, blank=True, null=True)
    monto = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True, null=True)

class codigoUsado(models.Model):
    codigo = models.ForeignKey(codigoAprobacion, on_delete=models.CASCADE, blank=True, null=True)
    factura = models.ForeignKey(factura, on_delete=models.CASCADE, blank=True, null=True)
    codigoFinanciero = models.ForeignKey(codigoFinanciero, on_delete=models.CASCADE, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    montoUsado = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True, null=True)
    usuario = models.CharField(max_length=255, blank=True, null=True)

