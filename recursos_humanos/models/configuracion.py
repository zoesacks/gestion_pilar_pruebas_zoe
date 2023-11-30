from django.db import models
from django.core.validators import MinValueValidator

SEXO = [
    ("F", "femenino"), 
    ("M", "masculino"),
]

class TipoDeDocumento(models.Model):
    numero = models.IntegerField(unique=True, validators=[MinValueValidator(0)])
    descripcion = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.descripcion)
 

class Nacionalidad(models.Model):
    numero = models.IntegerField(unique=True, validators=[MinValueValidator(0)])
    descripcion = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.descripcion)
    
class EstodoCivil(models.Model):
    numero = models.IntegerField(unique=True, validators=[MinValueValidator(0)])
    descripcion = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.descripcion)
    

class TipoEstudio(models.Model):
    numero = models.IntegerField(unique=True, validators=[MinValueValidator(0)])
    descripcion = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.descripcion)
    
class Escolariodad(models.Model):
    numero = models.IntegerField(unique=True, validators=[MinValueValidator(0)])
    descripcion = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.descripcion)
    
class Relacion(models.Model):
    numero = models.IntegerField(unique=True, validators=[MinValueValidator(0)])
    descripcion = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.descripcion)
    
class Particion(models.Model):
    numero = models.IntegerField(unique=True)
    descripcion = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.descripcion)
    
class Oficina(models.Model):
    numero = models.IntegerField(unique=True)
    descripcion = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.descripcion)
    
class Cargo(models.Model):
    numero = models.IntegerField(unique=True)
    descripcion = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.descripcion)
    
class Categoria(models.Model):
    numero = models.IntegerField(unique=True)
    descripcion = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.descripcion)
    

class TipoLicencia(models.Model):
    descripcion = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.descripcion)
    

class Provincia(models.Model):
    numero = models.IntegerField(unique=True, validators=[MinValueValidator(0)])
    descripcion = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.descripcion)
    
class Localidad(models.Model):
    numero = models.IntegerField(unique=True, validators=[MinValueValidator(0)])
    descripcion = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.descripcion)
    
