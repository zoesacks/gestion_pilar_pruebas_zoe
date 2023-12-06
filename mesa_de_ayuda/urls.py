from django.urls import path, include, re_path
<<<<<<< HEAD
from .views import SolicitudDeAyudaView, NuevaFotoView, NuevoComentarioView, mesaDeAyuda

=======
from .views import SolicitudDeAyudaView,NuevoComentarioView, mesaDeAyuda
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
>>>>>>> 1bf5648b9044416ef9b554405d6dee9aef70e38b

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
<<<<<<< HEAD
    path('api/<int:pk>/nueva-foto/', NuevaFotoView.as_view(), name='nueva-foto'),
    path('api/<int:pk>/nuevo-comentario/', NuevoComentarioView.as_view(), name='nuevo-comentario'),
]
=======
    path('api/<int:pk>/nuevo-comentario/', NuevoComentarioView.as_view(), name='nuevo-comentario'),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

>>>>>>> 1bf5648b9044416ef9b554405d6dee9aef70e38b
