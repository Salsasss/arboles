from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.auth.forms import UserCreationForm

from apps.especies.models import Especie, Taxonomia, EspecieDetalle, Url
from .models import Usuario

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
            
class RegistroForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, label='Nombre')
    last_name = forms.CharField(max_length=100, required=True, label='Apellido')
    email = forms.EmailField(required=True, label='Email')
    
    class Meta:
        model = Usuario
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado")
        return email