from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import GenerarTransferenciaSerializer, ConfirmarTransferenciaSerializer
from django.utils import timezone


def expedientes(request):
    return render(request, 'expedientes.html')


class GenerarTransferenciaView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = GenerarTransferenciaSerializer(data=request.data)
        if serializer.is_valid():
            # Llama al método create del serializador
            resultado = serializer.save()
            return Response(resultado, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmarTransferenciaView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ConfirmarTransferenciaSerializer(data=request.data)
        if serializer.is_valid():
            # Llama al método create del serializador
            resultado = serializer.save()
            return Response(resultado, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
