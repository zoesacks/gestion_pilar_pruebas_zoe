from django.urls import path, include, re_path
from .views import SolicitudDeAyudaView, NuevaFotoView, NuevoComentarioView, mesaDeAyuda



urlpatterns = [
    path('', mesaDeAyuda, name='mesaDeAyuda'),
    path('api/', SolicitudDeAyudaView.as_view(), name='solicitudDeAyuda'),
    path('api/<int:pk>/nueva-foto/', NuevaFotoView.as_view(), name='nueva-foto'),
    path('api/<int:pk>/nuevo-comentario/', NuevoComentarioView.as_view(), name='nuevo-comentario'),
]

