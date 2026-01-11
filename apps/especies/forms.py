from django import forms

from .models import Galeria

class GaleriaForm(forms.ModelForm):
    class Meta:
        model = Galeria
        exclude = ['autor']