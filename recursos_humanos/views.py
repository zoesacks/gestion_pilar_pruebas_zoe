from django.shortcuts import render
from django.views import View

from .models import Legajo, DatosPersonales

def construir_estructura_organigrama(legajos):
    # Crear un diccionario para mapear IDs de empleados a sus datos

    legajos_dict = {legajo.id: 
                    {"id": legajo.id, 
                     "puesto": legajo.cargo.descripcion, 
                     "nombre": DatosPersonales.objects.get(legajo=legajo).nombre, 
                     "hijos": []} 
                     for legajo in legajos}

    # Encontrar el empleado raíz (sin jefe)
    data = None
    for legajo in legajos:
        if not legajo.superior_inmediato:
            data = legajos_dict[legajo.id]

    # Organizar empleados bajo su jefe correspondiente
    for legajo in legajos:
        if legajo.superior_inmediato:
            jefe_id = legajo.superior_inmediato.id
            legajos_dict[jefe_id]["hijos"].append(legajos_dict[legajo.id])
    
    return data


# Luego, en tu vista, puedes utilizar esta función para obtener los datos
class OrganigramaView(View):
    template_name = 'organigrama_template.html'

    def get_context_data(self, **kwargs):
        legajos = Legajo.objects.all()
        data = construir_estructura_organigrama(legajos)

        context = {
            'data': data,
        }
        
        return context
    
        

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)