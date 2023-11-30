from django.db import models
from .configuracion import *


class Legajo(models.Model):
    num_legajo = models.IntegerField(unique=True)
    particion =  models.ForeignKey(Particion, on_delete=models.PROTECT)
    oficina = models.ForeignKey(Oficina, on_delete=models.PROTECT)
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    superior_inmediato = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='legajos_subalternos')

    #antiguedad
    ingreso = models.DateField()
    egreso = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.num_legajo}"


