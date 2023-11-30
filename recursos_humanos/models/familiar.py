from django.db import models
from django.core.validators import MinValueValidator
from .datosPersonales import TipoDeDocumento
from .legajo import Legajo
from .configuracion import *

class Familiar(models.Model):
    legajo = models.ForeignKey(Legajo, on_delete=models.CASCADE)
    relacion = models.ForeignKey(Relacion, on_delete=models.PROTECT)
    tipo_doc = models.ForeignKey(TipoDeDocumento, on_delete=models.PROTECT)
    num_doc = models.IntegerField(validators=[MinValueValidator(0)])
    apellido = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField()
    fecha_defuncion = models.DateField(blank=True, null=True)