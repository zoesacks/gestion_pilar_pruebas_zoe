from django.urls import path
from ingresos.views import aplicaciones_ingresos,calculadora,serivicios_generales

urlpatterns = [
    path('aplicaciones/', aplicaciones_ingresos, name='aplicaciones_ingresos'),
    path('calculadora/', calculadora, name='calculadora'),
    path('serivicios_generales/', serivicios_generales, name='serivicios_generales'),

]
