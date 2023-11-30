from django.db import models
from django.core.validators import MinValueValidator
from .legajo import Legajo
from .configuracion import *

class Domicilio(models.Model):
    #CAMPOS OBLIGATORIOS
    legajo = models.ForeignKey(Legajo, on_delete=models.CASCADE)
    provincia = models.ForeignKey(Provincia, on_delete=models.PROTECT)
    localidad = models.ForeignKey(Localidad, on_delete=models.PROTECT)
    calle = models.CharField(max_length=255)
    altura = models.IntegerField(validators=[MinValueValidator(0)])

    #CAMPOS OPCIONALES
    piso = models.CharField(max_length=255, blank=True, null=True)
    depto = models.CharField(max_length=255, blank=True, null=True)
    cod_postal = models.CharField(max_length=255, blank=True, null=True)
    pin = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.provincia}, {self.localidad}"