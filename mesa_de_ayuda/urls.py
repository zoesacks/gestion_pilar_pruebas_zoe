from django.urls import path, include, re_path
from .views import SolicitudDeAyudaView, NuevaFotoView, NuevoComentarioView



urlpatterns = [
    path('', SolicitudDeAyudaView.as_view(), name='mesaDeAyuda'),
    path('<int:pk>/nueva-foto/', NuevaFotoView.as_view(), name='nueva-foto'),
    path('<int:pk>/nuevo-comentario/', NuevoComentarioView.as_view(), name='nuevo-comentario'),
]

