from django.urls import path

from tesoreria.views import *

urlpatterns = [
    path('aplicaciones/', aplicaciones_tesoreria, name='aplicaciones'),

]