from django import forms
from .models import Transferencia, Usuario

class TransferenciaForm(forms.ModelForm):
    class Meta:
        model = Transferencia
        fields = ['receptor', 'documento']

    def __init__(self, *args, **kwargs):
        super(TransferenciaForm, self).__init__(*args, **kwargs)

        # Filtra los usuarios excluyendo al usuario actual
        self.fields['receptor'].queryset = Usuario.objects.all()