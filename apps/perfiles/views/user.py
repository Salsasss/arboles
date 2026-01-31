from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, UpdateView
from ..models import Usuario
from ..utils import ROL_CHOICES, ESTADO_CHOICES
from ..forms import UsuarioAdminForm, UsuarioEditForm

class StaffRequireMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.rol == Usuario.Rol.STAFF or self.request.user.rol == Usuario.Rol.ADMIN
    
# Listar Usuarios
class UsuarioListView(StaffRequireMixin, ListView):
    model = Usuario
    template_name = "panel_usuarios.html"
    context_object_name = "usuarios"
    paginate_by = 12
    
    def get_queryset(self):
        queryset = self.model.objects.get_queryset()
        
        if self.request.user.rol == Usuario.Rol.STAFF: # Si es STAFF -> Solo muestra MIEMBROS y a si mismo
            queryset = queryset.filter(
                Q(rol=Usuario.Rol.MIEMBRO) |
                Q(id_publico=self.request.user.id_publico)                
            )
            
        self.query = self.request.GET.get('query', '') # Buscador
        self.rol = self.request.GET.get('rol', '') # Filtro rol (MIEMBOR, STAFF o ADMIN)
        self.estado = self.request.GET.get('estado', '') # Filtro estado (Activo, Inactivo)
        
        # Buscador
        if self.query:
            queryset = queryset.filter(
                Q(username__icontains=self.query) |
                Q(first_name__icontains=self.query) |
                Q(last_name__icontains=self.query) |
                Q(email__icontains=self.query)
            )
            
        # Filtros
        if self.rol:
            queryset = queryset.filter(rol=self.rol)
            
        if self.estado:
            queryset = queryset.filter(is_active=self.estado)
            
        return queryset

    # Regresando el query para que se autocomplete en el buscador
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['ROL_CHOICES'] = ROL_CHOICES
        context['ESTADO_CHOICES'] = ESTADO_CHOICES
        context['query'] = self.query
        context['rol'] = self.rol
        context['estado'] = self.estado
         
        return context
    
# Crear Usuario
class UsuarioCreateView(StaffRequireMixin, CreateView):
    model = Usuario
    form_class = UsuarioAdminForm
    template_name = "usuario_form.html"
    success_url = reverse_lazy('panel')

# Editar Usuario
class UsuarioUpdateView(StaffRequireMixin, UpdateView):
    model = Usuario
    form_class = UsuarioEditForm
    template_name = "usuario_form.html"
    slug_field = 'id_publico' # El campo de tu modelo
    slug_url_kwarg = 'id_publico' # El nombre del parámetro en la URL (urls.py)
    success_url = reverse_lazy('panel')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        if self.object == self.request.user: # Si el usuario se está editando a si mismo
            form.fields['rol'].disabled = True
                
        return form
    
    def form_valid(self, form):
        if self.object == self.request.user: # Si el usuario se está editando a si mismo
            nuevo_rol = form.cleaned_data.get('rol')
            
            # Si el dato llegó Y no es ADMIN, bloqueamos.
            if nuevo_rol and nuevo_rol != "ADMIN":
                messages.error(self.request, "⚠️ Acción denegada: No puedes dejar de ser Administrador.")
                return redirect('panel') # O la url que prefieras
        
        # Si todo está bien, guardamos.
        return super().form_valid(form)
    
# Desactivar Usuario
class UsuarioDeleteView(StaffRequireMixin, DeleteView):
    model = Usuario
    template_name = "eliminar_objeto.html"
    context_object_name = "usuario"
    slug_field = 'id_publico' # El campo de tu modelo
    slug_url_kwarg = 'id_publico' # El nombre del parámetro en la URL (urls.py)
    success_url = reverse_lazy('panel')
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.rol == Usuario.Rol.STAFF:
            queryset = queryset.filter(rol=Usuario.Rol.MIEMBRO)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clase'] = "Usuario"
        context['accion'] = "Desactivar"
        context['success_url'] = reverse_lazy('panel')
        return context
        
    def form_valid(self, form):
        usuario_a_editar = self.object
        usuario_actual = self.request.user
        
        # ¿Se está desactivando a sí mismo?
        if usuario_a_editar == usuario_actual:
            messages.error(self.request, "⚠️ No puedes desactivarte ni quitarte permisos a ti mismo.")
            return redirect('panel')
        
        usuario_a_editar.soft_delete()
        return HttpResponseRedirect(self.get_success_url())
    
# Activar Usuario
class UsuarioActivarView(StaffRequireMixin, UpdateView):
    model = Usuario
    fields = []
    template_name = "activar_objeto.html"
    slug_field = 'id_publico' # El campo de tu modelo
    slug_url_kwarg = 'id_publico' # El nombre del parámetro en la URL (urls.py)
    success_url = reverse_lazy('panel')
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.rol == Usuario.Rol.STAFF:
            queryset = queryset.filter(rol=Usuario.Rol.MIEMBRO)
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clase'] = "Usuario"
        context['success_url'] = reverse_lazy('panel')
        return context
    
    def form_valid(self, form):
        self.object.activar()
        return super().form_valid(form)