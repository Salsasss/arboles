from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Especie, Taxonomia, EspecieDetalle, Galeria, Url

class EspecieForm(forms.ModelForm):
    descripcion = forms.CharField(widget=CKEditorUploadingWidget())
    
    class Meta:
        model = Especie
        exclude = ['slug', 'creador', 'is_active']

class TaxonomiaForm(forms.ModelForm):
    class Meta:
        model = Taxonomia
        exclude = ['especie']
        
class EspecieDetalleForm(forms.ModelForm):
    corteza = hojas = flores = frutos = semillas = biogeografia = importancia = forms.CharField(widget=CKEditorUploadingWidget(), required=False)
    
    class Meta:
        model = EspecieDetalle
        exclude = ['especie']
        
class UrlForm(forms.ModelForm):
    class Meta:
        model = Url
        exclude = ['especie']

class GaleriaForm(forms.ModelForm):
    class Meta:
        model = Galeria
        exclude = ['autor']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if 'especie' in self.fields:
            self.fields['especie'].queryset = Especie.all_objects.all()