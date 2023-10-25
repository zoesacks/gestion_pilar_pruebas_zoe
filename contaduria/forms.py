from django import forms
from .widgets import CustomMonthSelectWidget
from .models import proyeccionGastos,proyeccionIngresos

class ProyeccionGastosForm(forms.ModelForm):
    class Meta:
        model = proyeccionGastos
        fields = '__all__'
        widgets = {
            'MES': CustomMonthSelectWidget(),
        }

class ProyeccionIngresosForm(forms.ModelForm):
    class Meta:
        model = proyeccionIngresos
        fields = '__all__'
        widgets = {
            'MES': CustomMonthSelectWidget(),
        }