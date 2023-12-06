from rest_framework import serializers
from .models import SolicitudDeAyuda, ComentarioSolicutudDeAyuda
from django.contrib.auth.models import User


class ComentarioSolicutudSerializer(serializers.ModelSerializer):
    class Meta:
        model =  ComentarioSolicutudDeAyuda
        fields = '__all__' 
    


class SolicitudDeAyudaSerializer(serializers.ModelSerializer):
    comentarios = ComentarioSolicutudSerializer(many=True, required=False)

    class Meta: 
        model = SolicitudDeAyuda
        fields = '__all__' 

