
from django.contrib import admin
from django.urls import path,include
from ingresos.views import home,login_view,sin_acceso_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('sin_acceso/', sin_acceso_view, name='sin_acceso'),
    path('login/', login_view, name='login'),
    path('ingresos/', include('ingresos.urls')),
    path('contaduria/', include('contaduria.urls')),
    path('solicitud/', include('solicitud.urls')),
    path('factura/', include('facturas.urls')),
    path('tesoreria/', include('tesoreria.urls')),
]
