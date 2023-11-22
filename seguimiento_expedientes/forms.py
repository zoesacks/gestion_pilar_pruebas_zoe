from django import forms
from .models import Documento
from django.utils import timezone

class DocumentoForm(forms.Form):
    destinatario = forms.CharField(max_length=100)
    observacion = forms.CharField(widget=forms.Textarea)
    documento = forms.FileField()
    
'''
    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['en_transito'] = True
        cleaned_data['fecha_transito'] = timezone.now().date()
        return cleaned_data
'''