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
        read_only_fields = ('sector', 'fecha_alta')


class TransferenciaSerializer(serializers.Serializer):
    id_documento = serializers.IntegerField(required=True)
    id_usuario = serializers.IntegerField(required=False, allow_null=True)
    observacion = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        id_documento = validated_data.get('id_documento')
        id_usuario = validated_data.get('id_usuario')
        observacion = validated_data.get('observacion', '')

        doc = Documento.objects.get(id = id_documento)
        
        if(doc.en_transito == False):
            try:
                destinatario = Usuario.objects.get(id = id_usuario)
                doc.transferir(destinatario, observacion)

                return {'transferencia_exitosa': True, 'mensaje': 'Transferencia realizada correctamente'}
            
            except Documento.DoesNotExist:
                raise serializers.ValidationError("Documento no encontrado")
            
            except Usuario.DoesNotExist:
                raise serializers.ValidationError("Usuario no encontrado")

            except Exception:
                raise serializers.ValidationError("No se pudo realizar la transferencia")
        
        else:
            try:
                doc = Documento.objects.get(id = id_documento)
                doc.confirmarTransferencia()

                return {'transferencia_exitosa': True, 'mensaje': 'Se a confirmado la transferencia correctamente'}
            
            except Documento.DoesNotExist:
                raise serializers.ValidationError("Documento no encontrado")

            except Exception:
                raise serializers.ValidationError("No se pudo realizar la transferencia")


