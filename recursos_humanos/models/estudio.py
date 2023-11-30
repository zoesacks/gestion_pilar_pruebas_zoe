from django.db import models
from .legajo import Legajo
from .configuracion import *
    
class Estudio(models.Model):
    legajo = models.ForeignKey(Legajo, on_delete=models.CASCADE)
    tipo_estudio = models.ForeignKey(TipoEstudio, on_delete=models.PROTECT)
    escolaridad = models.ForeignKey(Escolariodad, on_delete=models.PROTECT)
    inicio = models.DateField()
    fin = models.DateField(blank=True, null=True)
    completo = models.BooleanField(default=False)