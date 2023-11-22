from .models  import Documento
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .serializers import DocumentoSerializer, UserSerializer
from django.contrib.auth.models import User


class DocumentoViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DocumentoSerializer

    def get_queryset(self):
        return Documento.objects.all()
    


class UsuarioLogueadoViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def list(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)