from django.db   import models
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils import timezone


class Sector(models.Model):
    nombre = models.CharField(max_length = 255, blank=False, null = False, unique=True)

    def __str__(self):
        return f'{self.nombre}'
    
    class Meta:
        verbose_name = 'sector'
        verbose_name_plural ='Sectores'

    def clean(self):   
        super().clean() 


class Usuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return f'{self.usuario} - {self.sector}'
    
    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural ='Usuarios'


class TipoDocumento(models.Model):
    numero = models.IntegerField(blank=False, null=False, unique=True)
    descripcion = models.CharField(max_length = 255, blank=False, null = False)

    def __str__(self):
        return f'{self.numero}'
    
    class Meta:
        verbose_name = 'tipo de documento'
        verbose_name_plural ='Tipos de documentos'

    def clean(self):
        super().clean() 


class Documento(models.Model):
    tipo = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE, blank=False, null=False)
    numero = models.IntegerField(blank=False, null=False)
    ejercicio = models.CharField(max_length = 4, blank=False, null=False)

    fecha_alta = models.DateField(auto_now_add=True, blank=True, null=True)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, blank=False, null=False)
    propietario = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=False, null=False, related_name="propietario")

    en_transito = models.BooleanField(default=False)
    destinatario = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True, null=True, related_name="destinatario")

    def __str__(self):
        return f'{self.tipo.descripcion}. Nro:  {self.tipo}-{self.numero},  {self.ejercicio}'
    
    class Meta:
        verbose_name = 'documento'
        verbose_name_plural ='Documentos'

    def clean(self):
        super().clean() 

    def save(self, *args, **kwargs):
        if self.existe():
            raise ValidationError("El documento ya esta registrado en el sistema")
        
        self.sector = self.propietario.sector
        
        super(Documento, self).save(*args, **kwargs)

    def existe(instance):
        return Documento.objects.filter(tipo = instance.tipo, numero = instance.numero, ejercicio = instance.ejercicio).exclude(pk=instance.pk).exists()
    

class Transferencia(models.Model):
     
    #Campos obligatorios
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, blank=False, null=False)
    receptor = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=False, null=False, related_name="receptor")

    #Campos que se autocomplentan al hacer el save
    fecha = models.DateField(blank=False, null=False)
    emisor = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=False, null=False, related_name="emisor")

    #extra
    observacion = models.TextField(blank=True, null=True)

    fecha_confirmacion = models.DateField(blank=True, null=True)
    recepcion_confirmada = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.documento}'
    
    class Meta:
        verbose_name = 'transferencia'
        verbose_name_plural ='Transferencias'

    def clean(self):
        if self.documento.propietario == self.receptor:
            raise ValidationError("No podes hacer una transferencia a vos mismo")
        
        if Transferencia.objects.filter(documento = self.documento, recepcion_confirmada = False).exists():
            raise ValidationError("El documento ya esta en transito")
        
        super().clean()

    def save(self, *args, **kwargs):
        if self.documento.propietario == self.receptor and Transferencia.objects.exclude(id=self.id).filter(documento = self.documento, recepcion_confirmada = False).exists():
            return
        
        self.emisor =  self.documento.propietario
        self.fecha = timezone.now()
        
        super(Transferencia, self).save(*args, **kwargs)

    @property
    def estado(self):
        if self.recepcion_confirmada == False:
            return "En transito"

        return "Recepcion confirmada"

    def confirmarRecepcion(self):
        if self.recepcion_confirmada == False:

            self.recepcion_confirmada = True
            self.save()

            documento = self.documento
            documento.sector = self.receptor.sector
            documento.propietario = self.receptor
            documento.ultima_actualizacion = timezone.now()
            documento.save()



