from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .models import Usuario
from .forms import RegistroForm

def redirect_home(request):
    if request.user.is_authenticated and (request.user.rol == Usuario.Rol.STAFF or request.user.rol == Usuario.Rol.ADMIN):
        return redirect('panel:mis_especies')
    return redirect('public:catalogo_especies')

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
        context['texto2'] = "¿Ya tienes una cuenta?"
        context['url_back'] = reverse_lazy('login')
        return context
    
class CustomPasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = "registration/login.html"
    success_url = reverse_lazy("cambiar_password")
    success_message = "Contraseña Actualizada Correctamente"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Cambiar Contraseña"
        context['texto1'] = "Cambia la contraseña de tu cuenta de Miembro"
        context['texto2'] = "¿Ya tienes una cuenta?"
        context['url_back'] = reverse_lazy('login')
        return context