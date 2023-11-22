from django.urls import path
from . import views

from rest_framework import routers
from .api import DocumentoViewSet

urlpatterns = [
    path('', views.expedientes, name='expedientes'),
]

router = routers.DefaultRouter()
router.register('api/documentos', DocumentoViewSet, 'documentos')
urlpatterns += router.urls