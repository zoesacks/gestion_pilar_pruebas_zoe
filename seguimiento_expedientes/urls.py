from django.urls import path, include, re_path
from rest_framework import routers
from .views import expedientes, TransferenciaView
from .api import DocumentoViewSet, UsuarioLogueadoViewSet, UsuariosViewSet

from rest_framework import routers, permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Seguimiento de expedientes API",
      default_version='v1',
      description="Descripción de tu API",
      terms_of_service="https://www.tuapi.com/terms/",
      contact=openapi.Contact(email="contact@tuapi.com"),
      license=openapi.License(name="Tu Licencia"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# Crear el router principal
router = routers.DefaultRouter()

router.register('documentos', DocumentoViewSet, 'documentos')
router.register('usuarioLogueado', UsuarioLogueadoViewSet, 'usuarioLogueado')
router.register('usuarios', UsuariosViewSet, 'usuarios')


urlpatterns = [
    path('', expedientes, name='expedientes'),
    path('api/transferencia/', TransferenciaView.as_view(), name='generarTransferencia'),
    path('api/', include(router.urls)),  

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]