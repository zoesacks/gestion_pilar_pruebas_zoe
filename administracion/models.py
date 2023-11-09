# ------------------------------------------------------------------------------------------
# Sistema de administracion - Ministerio de Desarrollo - Pilar
# Desarrollador Kevin Turkienich
# Julio 2023
# Kevin_turkienich@outlook.com
# ------------------------------------------------------------------------------------------

# Modelado de bases de datos para altas, bajas y modificaciones de datos maestros.

# ------------------------------------------------------------------------------------------
# Modulos importados
from django.db import models
# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE FONDOS
class proveedor(models.Model):
    ESTADO = models.BooleanField(default=0)
    CODIGO = models.CharField(max_length=50,null=False, blank=False)
    TIPO = models.CharField(max_length=50,null=True, blank=True)
    RAZON_SOCIAL = models.CharField(max_length=255, null=True, blank=True)
    DOMICILIO = models.CharField(max_length=255, null=True, blank=True) 
    FECHA_INSCRIPCION = models.DateField(null=True, blank=True)
    CUIT = models.CharField(max_length=255, null=True, blank=True)
    RAMO = models.CharField(max_length=255, null=True, blank=True)
    COMENTARIO = models.CharField(max_length=255, null=True, blank=True)

    

    def __str__(self):
        NAME = str(self.CODIGO) + " - " + str(self.TIPO) + " - " + str(self.RAZON_SOCIAL)
        return NAME
    
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural ='Proveedores' 

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE FONDOS
class fondo(models.Model):
    CODIGO = models.CharField(max_length=20,unique=True,null=False, blank=False)
    NOMBRE = models.CharField(max_length=120, null=False, blank=False)

    def __str__(self):
        NAME = str(self.CODIGO) + " - " + str(self.NOMBRE)
        return NAME
    
    class Meta:
        verbose_name = 'Fondo'
        verbose_name_plural ='Fondos' 

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE FONDOS
class concepto(models.Model):
    NOMBRE = models.CharField(max_length=120, null=False, blank=False,unique=True)

    def __str__(self):
        NAME = str(self.NOMBRE)
        return NAME
    
    class Meta:
        verbose_name = 'Concepto'
        verbose_name_plural ='Conceptos' 

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE EQUIVALENCAIS
class Equivalencia(models.Model):
    OrigenProgramatica = models.CharField(max_length=255)
    Descripcion = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Equivalencia'
        verbose_name_plural ='Equivalencias' 

    def __str__(self):
        return f"{self.OrigenProgramatica} | {self.Descripcion}"
    
# ------------------------------------------------------------------------------------------  
# ------------------------------------------------------------------------------------------
# CLASE FONDOS
class recurso(models.Model):
    CODIGO = models.CharField(verbose_name='Agrupamiento',max_length=50,unique=True,null=False, blank=False)
    NOMBRE = models.CharField(verbose_name='Descripcion',max_length=2550, null=False, blank=False)


    def __str__(self):
        NAME = f'{self.CODIGO} - {self.NOMBRE}'
        return NAME
    
    class Meta:
        verbose_name = 'Recurso'
        verbose_name_plural ='Recursos' 

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE FONDOS
class codigoFinanciero(models.Model):
    CODIGO = models.CharField(max_length=20,unique=True,null=False, blank=False)
    NOMBRE = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        NAME = str(self.CODIGO) + " - " + str(self.NOMBRE)
        return NAME
    
    class Meta:
        verbose_name = 'Codigo'
        verbose_name_plural ='Codigos financieros' 

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------

# CLASE DESARROLLADOR
class desarrollador(models.Model):
    LEGAJO = models.CharField(max_length=20,unique=True,null=False, blank=False)
    NOMBRE = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        NAME = str(self.LEGAJO) + " - " + str(self.NOMBRE)
        return NAME
    
    class Meta:
        verbose_name = 'Desarrollador'
        verbose_name_plural ='Desarrolladores' 

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------