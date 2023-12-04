
from django.contrib import admin
from django.urls import path,include
from ingresos.views import home,login_view,sin_acceso_view,logout_view#,about
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('sin_acceso/', sin_acceso_view, name='sin_acceso'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    #path('about/', about, name='about'),
    path('ingresos/', include('ingresos.urls')),
    path('contaduria/', include('contaduria.urls')),
    path('solicitud/', include('solicitud.urls')),
    path('factura/', include('facturas.urls')),
    path('tesoreria/', include('tesoreria.urls')),
    path('expedientes/', include('seguimiento_expedientes.urls')),
    path('recursos_humanos/', include('recursos_humanos.urls')),
] 


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)