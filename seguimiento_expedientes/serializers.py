from rest_framework import serializers
from .models import Documento, Sector, TipoDocumento, Usuario, Transferencia
from django.contrib.auth.models import User


class TipoDocumentoSerializer(serializers.ModelSerializer):
    class Meta: 
        model = TipoDocumento
        fields = '__all__' 

class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = '__all__' 

class UsuarioSerializer(serializers.ModelSerializer):
    sector = SectorSerializer()
    
    class Meta: 
        model = Usuario
        fields = '__all__' 

class DocumentoSerializer(serializers.ModelSerializer):
    tipo = TipoDocumentoSerializer() 
    propietario = UsuarioSerializer()
    destinatario = UsuarioSerializer()
    sector = SectorSerializer()

    class Meta:
        model =  Documento
        fields = '__all__' 
        read_only_fields = ('sector', 'fecha_alta',)

class TransferenciaSerializer(serializers.ModelSerializer):
    documento = SectorSerializer()
    receptor = UsuarioSerializer()
    emisor = UsuarioSerializer()

    class Meta: 
        model = Transferencia
        fields = '__all__' 
