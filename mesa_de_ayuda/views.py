from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import SolicitudDeAyuda, FotoSolicutudDeAyuda, ComentarioSolicutudDeAyuda
from .serializers import SolicitudDeAyudaSerializer
from django.shortcuts import get_object_or_404


def obtener_solicitud_o_404(pk):
    queryset = SolicitudDeAyuda.objects.all()
    return get_object_or_404(queryset, pk=pk)

def agregarfoto(solicitud, imagen):
    nueva_foto = FotoSolicutudDeAyuda(imagen=imagen)
    nueva_foto.save()
    solicitud.fotos.add(nueva_foto)

def agregarComentario(solicitud, comentario, usuario):
    nuevo_comentario = ComentarioSolicutudDeAyuda(comentario=comentario, usuario=usuario)
    nuevo_comentario.save()
    solicitud.comentarios.add(nuevo_comentario)


def mesaDeAyuda(request):
    
    context = {
    }

    return render(request, 'mesaDeAyuda.html', context)

class NuevaFotoView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        solicitud = obtener_solicitud_o_404(pk)
        imagen = request.data.get('imagen', None)
        agregarfoto(solicitud, imagen)
        return Response(status=status.HTTP_201_CREATED)

class NuevoComentarioView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        solicitud = obtener_solicitud_o_404(pk)
        comentario = request.data.get('comentario', None)
        agregarComentario(solicitud, comentario, request.user)
        return Response(status=status.HTTP_201_CREATED)
    

class SolicitudDeAyudaView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        instancias = SolicitudDeAyuda.objects.filter(usuario=request.user)
        serializador = SolicitudDeAyudaSerializer(instancias, many=True)
        datos_serializados = serializador.data
        return Response(datos_serializados)
    
    def post(self, request):
        datos_solicitud = request.data
        datos_solicitud['usuario'] = request.user.id
        serializador = SolicitudDeAyudaSerializer(data=datos_solicitud)
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data, status=status.HTTP_201_CREATED)
        return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)