from django.db import models
from django.core.validators import MinValueValidator
from django.core.validators import FileExtensionValidator
from .legajo import Legajo
from .configuracion import *


class DatosPersonales(models.Model):
    #CAMPOS OBLIGATORIOS
    legajo = models.ForeignKey(Legajo, on_delete=models.CASCADE)
    tipo_doc = models.ForeignKey(TipoDeDocumento, on_delete=models.PROTECT)
    num_doc = models.IntegerField(validators=[MinValueValidator(0)])
    cuit = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="cuit/cuil")
    sexo = models.CharField(max_length=255, choices=SEXO)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    nacionalidad = models.ForeignKey(Nacionalidad, on_delete=models.PROTECT)
    estado_civil = models.ForeignKey(EstodoCivil, on_delete=models.PROTECT)
    nacimiento = models.DateField()
    foto = models.ImageField(
        upload_to='img/', 
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])],)
    
    #CAMPOS OPCIONALES
    defuncion = models.DateField(blank=True, null=True)
    matricula = models.CharField(max_length=255, blank=True, null=True)
    discapacitado = models.BooleanField(default=False)
    ganancias = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.apellido}, {self.nombre}"
    


