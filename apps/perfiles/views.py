from django.views.generic.edit import CreateView
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
    template_name = "registration/register.html"
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        usuario = form.save()
        login(self.request, usuario)
        return redirect(self.success_url)