from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
<<<<<<< HEAD
from .models import SolicitudDeAyuda, FotoSolicutudDeAyuda, ComentarioSolicutudDeAyuda
from django.contrib.auth.models import User
=======
from .models import SolicitudDeAyuda, ComentarioSolicutudDeAyuda
>>>>>>> 1bf5648b9044416ef9b554405d6dee9aef70e38b
from .serializers import SolicitudDeAyudaSerializer
from django.shortcuts import get_object_or_404


def obtener_solicitud_o_404(pk):
    queryset = SolicitudDeAyuda.objects.all()
    return get_object_or_404(queryset, pk=pk)

def agregarfoto(solicitud, imagen, usuario):
    nuevo_comentario = ComentarioSolicutudDeAyuda(imagen=imagen, usuario=usuario)
    nuevo_comentario.save()
    solicitud.comentarios.add(nuevo_comentario)

def agregarComentario(solicitud, comentario, usuario):
    nuevo_comentario = ComentarioSolicutudDeAyuda(comentario=comentario, usuario=usuario)
    nuevo_comentario.save()
    solicitud.comentarios.add(nuevo_comentario)

<<<<<<< HEAD

def mesaDeAyuda(request):
    
    context = {
    }

    return render(request, 'mesaDeAyuda.html', context)

class NuevaFotoView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
=======
>>>>>>> 1bf5648b9044416ef9b554405d6dee9aef70e38b

def mesaDeAyuda(request):
    
    context = {
    }

    return render(request, 'mesaDeAyuda.html', context)



class NuevoComentarioView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        solicitud = obtener_solicitud_o_404(pk)
        comentario = request.data.get('comentario', None)
        imagen = request.data.get('imagen', None)

        if comentario:
            agregarComentario(solicitud, comentario, request.user)

        if imagen:
            agregarfoto(solicitud, imagen, request.user)

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
        usuario_id = request.user.id
        datos_solicitud = {'usuario': usuario_id, **request.data}

        serializador = SolicitudDeAyudaSerializer(data=datos_solicitud)
        
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data, status=status.HTTP_201_CREATED)
        print(serializador.errors)
        return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)