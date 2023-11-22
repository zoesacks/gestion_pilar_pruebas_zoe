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


class Transferencia(models.Model):
  
    #Campos que se autocomplentan
    fecha = models.DateField(blank=False, null=False)
    emisor = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=False, null=False, related_name="emisor")
    receptor = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=False, null=False, related_name="receptor")
    fecha_confirmacion = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.fecha}, {self.emisor}'
    
    class Meta:
        verbose_name = 'transferencia'
        verbose_name_plural ='Transferencias'

    def clean(self):
        super().clean()

    def save(self, *args, **kwargs):
        super(Transferencia, self).save(*args, **kwargs)


class Documento(models.Model):
    #DATOS DEL DOCUMENTO
    tipo = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE, blank=False, null=False)
    numero = models.IntegerField(blank=False, null=False)
    ejercicio = models.CharField(max_length = 4, blank=False, null=False)
    propietario = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=False, null=False, related_name="propietario")
    #se autocompleta
    fecha_alta = models.DateField(auto_now_add=True, blank=True, null=True)
    
    
    #PARA CUANDO EL DOCUMENTO ESTA EN TRANSFERIA
    #obligatorio
    destinatario = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True, null=True, related_name="destinatario")

    #extra
    observacion = models.TextField(blank=True, null=True)

    #se autocompleta con el formulario
    en_transito = models.BooleanField(default=False)
    fecha_transito = models.DateField(blank=True, null=True)


    #HITORIAL DE TRANSFERENCIAS
    transferencias = models.ManyToManyField(Transferencia)

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
        
        super(Documento, self).save(*args, **kwargs)

    def existe(instance):
        return Documento.objects.filter(tipo = instance.tipo, numero = instance.numero, ejercicio = instance.ejercicio).exclude(pk=instance.pk).exists()
    




