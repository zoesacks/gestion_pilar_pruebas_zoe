from rest_framework import serializers
from .models import Documento, Sector, TipoDocumento, Usuario, Transferencia
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',)

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
    usuario = UserSerializer()

    class Meta: 
        model = Usuario
        fields = '__all__' 

class TransferenciaSerializer(serializers.ModelSerializer):
    emisor = UsuarioSerializer()
    receptor = UsuarioSerializer()

    class Meta: 
        model = Transferencia
        fields = '__all__' 

class DocumentoSerializer(serializers.ModelSerializer):
    tipo = TipoDocumentoSerializer() 
    propietario = UsuarioSerializer()
    destinatario = UsuarioSerializer()
    transferencias = TransferenciaSerializer(many=True)

    class Meta:
        model =  Documento
        fields = '__all__' 
        read_only_fields = ('sector', 'fecha_alta',)


