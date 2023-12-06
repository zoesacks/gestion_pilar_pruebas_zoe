from django.urls import path, include, re_path
from .views import SolicitudDeAyudaView,NuevoComentarioView, mesaDeAyuda
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Mesa de ayuda API",
      default_version='v1',
      description="Descripción de tu API",
      terms_of_service="https://www.tuapi.com/terms/",
      contact=openapi.Contact(email="contact@tuapi.com"),
      license=openapi.License(name="Tu Licencia"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', mesaDeAyuda, name='mesaDeAyuda'),
    path('api/', SolicitudDeAyudaView.as_view(), name='solicitudDeAyuda'),
    path('api/<int:solicitud_id>/', SolicitudDeAyudaView.as_view(), name='solicitud-detalle'),
    path('api/<int:pk>/nuevo-comentario/', NuevoComentarioView.as_view(), name='nuevo-comentario'),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

