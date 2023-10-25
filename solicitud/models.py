from django.db import models
from administracion.models import desarrollador
from django.contrib.auth.models import User
# Create your models here.

class mesa(models.Model):
    FECHA = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    TITULO = models.CharField(verbose_name="Descripcion corta",max_length=50,null=False, blank=False)
    DETALLE = models.TextField(verbose_name="Detalle prolongado (Opcional)",null=True, blank=True)
    USUARIO = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,verbose_name="Usuario solicitante",)
    DESARROLLADOR = models.ForeignKey(desarrollador,on_delete=models.CASCADE,null=True,blank=True,verbose_name="Desarrollador asignado")
    ESTADO = models.BooleanField(verbose_name="Completado",default=0)

    
    def __str__(self):
        NAME = "Solic: " + str(self.TITULO) + " - Estado: " + str(self.ESTADO)
        return NAME
    
    class Meta:
        verbose_name = 'Solicitud a mesa de ayuda'
        verbose_name_plural ='Mesa de ayuda' 


class solped(models.Model):
    CODIGO = models.CharField(max_length=50,null=False, blank=False)
    DETALLE = models.TextField(null=True, blank=True) 
    NUMERO = models.CharField(max_length=50,null=False, blank=False)
    FECHA = models.DateField(null=True, blank=True)
    TOTAL = models.DecimalField(max_digits=20,decimal_places=2,default=0,null=False, blank=False)
    NRO = models.CharField(max_length=255,blank=True,null=True) 
    SECRETARIA = models.CharField(max_length=255,blank=True,null=True)
    SECRETARIA_NOMBRE = models.CharField(max_length=255,blank=True,null=True)
    FONDO = models.CharField(max_length=255,blank=True,null=True)
    CATEGORIA = models.CharField(max_length=255,blank=True,null=True)
    FUENTE_FINANCIAMIENTO = models.CharField(max_length=255,blank=True,null=True)
    COMENTARIOS = models.CharField(max_length=50,null=True, blank=True)
    AUTORIZADO_POR = models.CharField(max_length=255,blank=True,null=True)
    FECHA_AUTORIZADO = models.DateTimeField(blank=True,null=True)
    ESTADO = models.BooleanField(default=0)
    OBSERVADA = models.BooleanField(default=0)
    
    def __str__(self):
        NAME = str(self.NUMERO) + " - " + str(self.DETALLE) + " - " + str(self.TOTAL)
        return NAME
    
    class Meta:
        verbose_name = 'Solicitud de pedido'
        verbose_name_plural ='Solicitudes de pedidos' 

    def save(self, *args, **kwargs):
        if self.COMENTARIOS is not None:
            if len(self.COMENTARIOS) > 1:
                self.OBSERVADA = True
            else:
                self.OBSERVADA = False
        else:
            self.OBSERVADA = False
        super(solped,self).save(*args, **kwargs)

    def TOTAL_SOLICITUD(self):
        total_cost = 0
        for producto in self.productopedido_set.all():
            if producto.precio_unitario is not None:
                total_cost += producto.precio_unitario * producto.cantidad

        total_cost = round(total_cost, 0)
        return total_cost

class productoPedido(models.Model):
    pedido = models.ForeignKey(solped, on_delete=models.CASCADE)
    articulo  = models.CharField(max_length=255,blank=True,null=True)
    cantidad = models.DecimalField(max_digits=20, decimal_places=2, default=1, blank=False, null=False)
    precio_unitario = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=False, null=False)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=False, null=False)
    objeto = models.CharField(max_length=255,blank=True,null=True)

    class Meta:
        verbose_name = 'Articulos'
        verbose_name_plural ='Articulos incluidos en la solicitud' 

    def save(self, *args, **kwargs):
        self.total = self.cantidad * self.precio_unitario
        super(productoPedido,self).save(*args, **kwargs)