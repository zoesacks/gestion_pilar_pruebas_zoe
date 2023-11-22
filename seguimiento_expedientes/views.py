from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Documento
from .serializers import DocumentoSerializer
from django.utils import timezone


def expedientes(request):
    return render(request, 'expedientes.html')


class GenerarTransferenciaView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = DocumentoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)