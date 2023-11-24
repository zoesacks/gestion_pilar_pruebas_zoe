from django.urls import path, include
from rest_framework import routers
from .views import expedientes, GenerarTransferenciaView, ConfirmarTransferenciaView

from rest_framework import routers
from .api import DocumentoViewSet, UsuarioLogueadoViewSet, UsuariosViewSet

# Crear el router principal
router = routers.DefaultRouter()

router.register('documentos', DocumentoViewSet, 'documentos')
router.register('usuarioLogueado', UsuarioLogueadoViewSet, 'usuarioLogueado')
router.register('usuarios', UsuariosViewSet, 'usuarios')


urlpatterns = [
    path('', expedientes, name='expedientes'),
    path('api/generarTransferencia/', GenerarTransferenciaView.as_view(), name='generarTransferencia'),
    path('api/confirmarTransferencia/', ConfirmarTransferenciaView.as_view(), name='confirmarTransferencia'),
    path('api/', include(router.urls)),  
]