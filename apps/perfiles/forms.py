from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from apps.especies.models import Especie, Taxonomia, EspecieDetalle

class EspecieForm(forms.ModelForm):
    descripcion = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Especie
        exclude = ['slug', 'creador']

class TaxonomiaForm(forms.ModelForm):
    class Meta:
        model = Taxonomia
        exclude = ['especie']
        
class EspecieDetalleForm(forms.ModelForm):
    corteza = hojas = flores = frutos = semillas = biogeografia = importancia = forms.CharField(widget=CKEditorUploadingWidget(), required=False)
    
    class Meta:
        model = EspecieDetalle
        exclude = ['especie']