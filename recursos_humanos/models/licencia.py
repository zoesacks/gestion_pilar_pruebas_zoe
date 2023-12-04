from django.db import models
from django.core.validators import MinValueValidator
from datetime import timedelta, date
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import F, ExpressionWrapper, fields, DateTimeField, Sum

from .legajo import Legajo
from .configuracion import *



class Licencia(models.Model):
    legajo = models.ForeignKey(Legajo, on_delete=models.CASCADE)
    dias = models.IntegerField(validators=[MinValueValidator(0)])
    tipo_licencia = models.ForeignKey(TipoLicencia, on_delete=models.PROTECT)
    dias_habiles = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.legajo}"
    

    
    @property
    def dias_pendientes(self):
        fechas_uso_licencia = UsoLicencia.objects.filter(licencia=self).values_list('fecha_inicio', 'fecha_fin')
        dias_habiles_usados = 0

        for fecha_inicio, fecha_fin in fechas_uso_licencia:
            if(self.dias_habiles):
                dias_habiles_usados += obtener_dias_habiles(fecha_inicio, fecha_fin)
            else:
                dias_habiles_usados += obtener_dias(fecha_inicio, fecha_fin)

        dias_totales_licencia = self.dias 
        dias_pendientes = dias_totales_licencia - dias_habiles_usados

        return dias_pendientes

class UsoLicencia(models.Model):
    licencia = models.ForeignKey(Licencia, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    observaciones = models.DateField(blank=True, null=True)
    certificado_foto = models.ImageField(upload_to='certificados/', null=True, blank=True)
    certificado_pdf = models.FileField(upload_to='certificados/', null=True, blank=True)
        
    def __str__(self):
        return f"{self.licencia}"
    
    def clean(self):
        super().clean() 

def es_dia_habil(fecha):
    return fecha.weekday() < 5 and not Feriado.objects.filter(fecha=fecha).exists() 

def obtener_dias_habiles(fecha_inicio, fecha_fin):
    dias_habiles = 0
    fecha_actual = fecha_inicio

    while fecha_actual <= fecha_fin:
        if es_dia_habil(fecha_actual):
            dias_habiles += 1
        fecha_actual += timedelta(days=1)

    return dias_habiles

def obtener_dias(fecha_inicio, fecha_fin):
    dias_habiles = 0
    fecha_actual = fecha_inicio

    while fecha_actual <= fecha_fin:
        dias_habiles += 1
        fecha_actual += timedelta(days=1)

    return dias_habiles