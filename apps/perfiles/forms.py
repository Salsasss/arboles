from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
            
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
    
class UsuarioAdminForm(RegistroForm):
    rol = forms.ChoiceField(
        choices=Usuario.Rol.choices,
        label="Rol",
        required=True,
        help_text="Define el rol del usuario."
    )

    field_order = ['username', 'first_name', 'last_name', 'email', 'rol']
    
    class Meta:
        model = Usuario
        fields = ('username', 'first_name', 'last_name', 'email', 'rol')
        
class UsuarioEditForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'rol']