from django.shortcuts import render, redirect
from .models import *
from django.db.models import Max,Subquery
from .forms import TransferenciaForm


def expedientes(request):


    return render(request, 'expedientes.html')


def crearTransferencia(request):
    user = request.user
    if request.method == 'POST':
        form = TransferenciaForm(request.POST, user=user)
        if form.is_valid():
            form.save()
            return redirect('expedientes')  # Redirige a una página exitosa
    else:
        form = TransferenciaForm()

    return form


def obtenerUsuarios(request):
    usuarios = Usuario.objects.exclude(usuario = request.user)
    return usuarios

def obtenerDocumentosPendientes(request):
    usuario = Usuario.objects.get(usuario = request.user)
    
    transferencias = Transferencia.objects.filter(receptor = usuario, recepcion_confirmada = False)
    documentosIDs = transferencias.values_list('documento', flat=True)

    documentos = Documento.objects.filter(id__in = documentosIDs)

    return documentos

def obtenerDocumentosEnTransito(request):
    usuario = Usuario.objects.get(usuario = request.user)

    transferencias = Transferencia.objects.filter(emisor = usuario, recepcion_confirmada = False)
    documentosIDs = transferencias.values_list('documento')

    documentos = Documento.objects.filter(id__in = documentosIDs)

    return list(documentos)

def obtenerDocumentos(request):
    usuario = Usuario.objects.get(usuario = request.user)
    transferencias = Transferencia.objects.filter(recepcion_confirmada = False)

    documentos = Documento.objects.filter(propietario = usuario).exclude(id__in=transferencias.values('documento'))

    return documentos 

     
