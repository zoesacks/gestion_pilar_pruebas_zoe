from django.db import models

# Create your models here.
class regimen(models.Model):
    NUMERO = models.IntegerField(blank=False,null=False)
    INCISO = models.CharField(max_length=2,blank=True,null=True)
    DESCRIPCION = models.CharField(max_length=255,blank=False,null=False)

    class Meta:
        verbose_name = 'Regimen'
        verbose_name_plural ='Tabla de regímenes' 

    def __str__(self):
        return f'{self.NUMERO} - (Inc. {self.INCISO}) {self.DESCRIPCION}'

class tabla_alicuotas(models.Model):
    REGIMEN = models.ForeignKey(regimen,on_delete=models.CASCADE,blank=False,null=False)
    CODIGO = models.CharField(max_length=15,blank=False,null=False)
    BASE_DESDE = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    BASE_HASTA = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    MONTO_FIJO  = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    ALICUOTA_REAL = models.DecimalField(max_digits=4,decimal_places=4,blank=False,null=False)
    ALICUOTA_PROYECTADA = models.DecimalField(max_digits=4,decimal_places=4,blank=True,null=True)

    class Meta:
        verbose_name = 'Alicuota'
        verbose_name_plural ='Tabla de alícuotas' 

    def __str__(self):
        return f'{self.REGIMEN} - Alicuota ({self.ALICUOTA_REAL})'

class base_contribuyentes(models.Model):
    CUENTA = models.IntegerField(blank=False,null=False)
    TITULAR = models.CharField(max_length=255,blank=False,null=False)
    BASE = models.DecimalField(max_digits=20,decimal_places=2,blank=False,null=False)
    REGIMEN = models.ForeignKey(regimen,on_delete=models.CASCADE,blank=False,null=False)

    class Meta:
        verbose_name = 'Contribuyente'
        verbose_name_plural ='Base de contribuyentes' 

    def alicuota_utilizada(self):
        alicuotas = tabla_alicuotas.objects.filter(REGIMEN=self.REGIMEN)
        base_impositiva = self.BASE
        for x in alicuotas:
            if base_impositiva > x.BASE_DESDE and base_impositiva <= x.BASE_HASTA:
                alicuota = x.ALICUOTA_REAL
        return alicuota
    
    def alicuota_proyectada(self):
        alicuotas = tabla_alicuotas.objects.filter(REGIMEN=self.REGIMEN)
        base_impositiva = self.BASE
        for x in alicuotas:
            if base_impositiva > x.BASE_DESDE and base_impositiva <= x.BASE_HASTA:
                alicuota = x.ALICUOTA_PROYECTADA
        return alicuota
    
    def impuesto(self):
        alicuotas = tabla_alicuotas.objects.filter(REGIMEN=self.REGIMEN)
        base_impositiva = self.BASE
        for x in alicuotas:
            if base_impositiva > x.BASE_DESDE and base_impositiva <= x.BASE_HASTA:
                total = ((base_impositiva - x.BASE_DESDE) * x.ALICUOTA_REAL) + x.MONTO_FIJO
        return total

    def impuesto_proyectado(self):
        alicuotas = tabla_alicuotas.objects.filter(REGIMEN=self.REGIMEN)
        base_impositiva = self.BASE
        for x in alicuotas:
            if base_impositiva > x.BASE_DESDE and base_impositiva <= x.BASE_HASTA:
                total = ((base_impositiva - x.BASE_DESDE) * x.ALICUOTA_PROYECTADA) + x.MONTO_FIJO
        return total