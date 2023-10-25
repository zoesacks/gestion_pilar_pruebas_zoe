from django.urls import path
from facturas.views import *

urlpatterns = [
    path('facturas/', facturas, name='facturas'),
    path('detalleFactura/<int:factura_detalle_id>/', detalleFactura, name='detalleFactura'),
]