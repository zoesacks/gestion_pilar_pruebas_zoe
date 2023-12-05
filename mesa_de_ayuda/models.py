from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.core.validators import FileExtensionValidator

ESTADO = [ 
    ("Pendiente","Pendiente"),
    ("En proceso","En proceso"),
    ("Terminado","Terminado")
]

class FotoSolicutudDeAyuda(models.Model):
    foto = models.ImageField(
        upload_to='img/', 
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])],)
    
    class Meta:
        verbose_name = 'Foto de solicitud a mesa de ayuda'
        verbose_name_plural ='Fotos de solicitudes a mesa de ayuda' 


class ComentarioSolicutudDeAyuda(models.Model):
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Comentario de solicitud a mesa de ayuda'
        verbose_name_plural ='Comentarios de solicitudes a mesa de ayuda' 

    def __str__(self):
        return "Usuario: " + str(self.usuario) + " .Coment.: " + self.comentario + "\n"


class SolicitudDeAyuda(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    titulo = models.CharField(max_length=50)
    detalle = models.TextField(null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="solicitante",)
    desarrollador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="desarrollador")
    estado = models.CharField(max_length=255, choices=ESTADO, default=('Pendiente'))

    fotos = models.ManyToManyField(FotoSolicutudDeAyuda)
    comentarios = models.ManyToManyField(ComentarioSolicutudDeAyuda)

    def __str__(self):
        NAME = "Solic: " + str(self.titulo) + " - Estado: " + str(self.estado)
        return NAME
    
    class Meta:
        verbose_name = 'Solicitud a mesa de ayuda'
        verbose_name_plural ='Solicitudes a mesa de ayuda' 

