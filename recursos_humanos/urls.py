from django.urls import path, include, re_path
from .views import OrganigramaView

urlpatterns = [
    path('organigrama/', OrganigramaView.as_view(), name='organigrama'),
]
