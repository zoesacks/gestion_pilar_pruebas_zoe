from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.models import Group
from django.utils import timezone
from zoneinfo import ZoneInfo

@admin.action(description="Autorizar")
def autorizarSolped(modeladmin, request, queryset):
    # Verificar si el usuario actual pertenece al grupo "Aprobadores"
    if request.user.groups.filter(name='Aprobadores').exists():
        for query in queryset:
            if query.ESTADO == 0:
                query.ESTADO = 1
                query.AUTORIZADO_POR = request.user.username
                query.FECHA_AUTORIZADO = timezone.now() - timezone.timedelta(hours=3)
                query.save()
        
        messages.success(request, "La/s Solicitud/es fueron aprobadas correctamente.")
    else:
        messages.error(request, "No tienes permisos para aprobar estas solicitudes.")


@admin.action(description="Cancelar autorizacion")
def cancelarSolped(modeladmin, request, queryset):
    # Verificar si el usuario actual pertenece al grupo "Aprobadores"
    if request.user.groups.filter(name='Aprobadores').exists():
        for query in queryset:
            if query.ESTADO == 1:
                query.ESTADO = 0
                query.save()
        
        messages.success(request, "La/s solicitud/es se modificaron correctamente.")
    else:
        messages.error(request, "No tienes permisos para cancelar la autorización de estas solicitudes.")