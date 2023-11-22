from django.urls import path, include
from rest_framework import routers
from .views import expedientes, GenerarTransferenciaView

from rest_framework import routers
from .api import DocumentoViewSet, UsuarioLogueadoViewSet

# Crear el router principal
router = routers.DefaultRouter()

router.register('documentos', DocumentoViewSet, 'documentos')
router.register('usuarioLogueado', UsuarioLogueadoViewSet, 'usuarioLogueado')


urlpatterns = [
    path('', expedientes, name='expedientes'),
    path('api/generarTransferencia/', GenerarTransferenciaView.as_view(), name='generarTransferencia-api'),
    path('api/', include(router.urls)),  
]