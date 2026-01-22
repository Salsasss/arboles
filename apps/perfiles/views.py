from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from .models import Usuario
from .forms import RegistroForm

def redirect_home(request):
    if request.user.is_authenticated and (request.user.rol == Usuario.Rol.STAFF or request.user.rol == Usuario.Rol.ADMIN):
        return redirect('panel:mis_especies')
    return redirect('public:catalogo_especies')

class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Iniciar Sesión'
        context['texto1'] = 'Ingresa tu cuenta de Miembro'
        context['footer'] = True
        context['reset'] = True
        context['texto2'] = '¿Aún no tienes cuenta?'
        context['texto3'] = 'Registrarse aquí'
        context['url'] = reverse_lazy('registrar')
        return context

class RegisterCreateView(CreateView):
    form_class = RegistroForm
    template_name = "registration/login.html"
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        usuario = form.save()
        login(self.request, usuario)
        return redirect(self.success_url)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrarse"
        context['texto1'] = "Crea tu cuenta de Miembro"
        context['footer'] = True
        context['texto2'] = "¿Ya tienes una cuenta?"
        context['texto3'] = "Inicia Sesión aquí"
        context['url'] = reverse_lazy('login')
        return context

class CustomPasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = "registration/login.html"
    success_url = reverse_lazy("cambiar_password")
    success_message = "Contraseña Actualizada Correctamente"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Cambiar Contraseña"
        context['texto1'] = "Cambia la contraseña de tu cuenta de Miembro"
        return context

# ¿Olvidaste tu contraseña?
# Paso 1
class CustomPasswordResetView(PasswordResetView):
    template_name = "registration/login.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Recuperar Contraseña"
        context['texto1'] = "Ingresa tu correo electrónico y te enviaremos instrucciones para restablecerla"
        return context
    
# Paso 3
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "registration/login.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Cambiar Contraseña"
        return context

# Paso 2
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "registration/mensaje.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Restablecimiento de contraseña enviado"
        context['texto1'] = "¡Listo! Revisa tu correo. > Te enviamos los pasos para cambiar tu contraseña. Si no aparece, verifica tu carpeta de spam."
        return context

# Paso 4
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "registration/mensaje.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Contraseña Restablecida"
        context['texto1'] = "¡Ha restablecido su contraseña exitosamente!"
        context['footer'] = True
        context['texto3'] = "Inicia Sesión aquí"
        context['url'] = reverse_lazy('login')
        return context