from django.db import models
from django.core.validators import MinValueValidator
from .legajo import Legajo
from .configuracion import *


class Licencia(models.Model):
    legajo = models.ForeignKey(Legajo, on_delete=models.CASCADE)
    dias = models.IntegerField(validators=[MinValueValidator(0)])
    tipo_licencia = models.ForeignKey(TipoLicencia, on_delete=models.PROTECT)
    dias_habiles = models.BooleanField(default=False)


class UsoLicencia(models.Model):
    licencia = models.ForeignKey(Licencia, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    observaciones = models.DateField(blank=True, null=True)
    certificado_foto = models.ImageField(upload_to='certificados/', null=True, blank=True)
    certificado_pdf = models.FileField(upload_to='certificados/', null=True, blank=True)