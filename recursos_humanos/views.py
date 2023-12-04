from django.shortcuts import render
import json
from django.views import View
from .models import Legajo, DatosPersonales
from django.conf import settings


def construir_estructura_organigrama(legajos):
    legajos_dict = []

    for legaj in legajos:
        legajo = {
            "id": legaj.id,
            "pid": legaj.superior_inmediato_id,
            "Nombre": DatosPersonales.objects.get(legajo=legaj).apellido + ", " + DatosPersonales.objects.get(legajo=legaj).nombre,
            "Puesto": legaj.cargo.descripcion,
            "img": DatosPersonales.objects.get(legajo=legaj).foto.name
        }
        print(legajo)
        legajos_dict.append(legajo)

    return legajos_dict

class OrganigramaView(View):
    template_name = 'organigrama_template.html'

    def get_context_data(self, **kwargs):
        legajos = Legajo.objects.all()
        data = construir_estructura_organigrama(legajos)
        data = json.dumps(data)
        context = {
            'MEDIA_URL': settings.MEDIA_URL,
            'data': data,
        }

        
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
