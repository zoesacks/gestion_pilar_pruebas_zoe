from .models  import Documento, Sector, TipoDocumento, Usuario, Transferencia
from rest_framework import viewsets, permissions
from .serializers import DocumentoSerializer


class DocumentoViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DocumentoSerializer

    def get_queryset(self):
        return Documento.objects.all()
    



