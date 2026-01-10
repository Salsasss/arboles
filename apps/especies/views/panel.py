from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.db import transaction

from apps.perfiles.models import Usuario
from apps.perfiles.forms import EspecieForm, TaxonomiaForm, EspecieDetalleForm
from ..utils import TIPO_CHOICES, ESTADO_CONSERVACION_CHOICES
from ..models import Especie

class StaffRequireMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.rol == Usuario.Rol.STAFF or self.request.user.rol == Usuario.Rol.ADMIN
    
# Listar Especies
class EspecieListView(ListView, StaffRequireMixin):
    model = Especie
    template_name = "staff/mis_especies.html"
    context_object_name = "especies"
    paginate_by = 8
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # queryset = self.model.all_objects.get_queryset() -> Trae todas incluso inactivas
        
        if self.request.user.rol == Usuario.Rol.STAFF:
            queryset = queryset.filter(creador=self.request.user) # Solo muestra las especies que yo cree
        
        self.query = self.request.GET.get('query', '') # Buscador
        self.tipo = self.request.GET.get('tipo', '') # Filtro tipo (Arbol, Palmera)
        self.estado = self.request.GET.get('estado', '') # Filtro estado IUCN (NE, DD, LC, NT, ...)
        
        # Buscador
        if self.query:            
            queryset = queryset.filter(
                Q(nombre_comun__icontains=self.query) |
                Q(nombre_cientifico__icontains=self.query) |
                Q(taxonomia__familia__icontains=self.query) |
                Q(taxonomia__genero__icontains=self.query)
            )
            
        #Filtros
        if self.tipo:
            queryset = queryset.filter(tipo=self.tipo)
            
        if self.estado:
            queryset = queryset.filter(estado_conservacion=self.estado)
    
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Buscador
        context['query'] = self.query
        
        # Filtros
        context['TIPO_CHOICES'] = TIPO_CHOICES
        context['ESTADO_CONSERVACION_CHOICES'] = ESTADO_CONSERVACION_CHOICES
        context['tipo'] = self.tipo
        context['estado'] = self.estado
        
        return context
    
# Crear Especie
class EspecieCreateView(CreateView, StaffRequireMixin):
    model = Especie
    form_class = EspecieForm
    template_name = "staff/especie_form.html"
    success_url = reverse_lazy('panel:mis_especies')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Si se envió el formulario (POST), recuperamos los datos ingresados
        if self.request.POST:
            context['form_taxonomia'] = TaxonomiaForm(self.request.POST, prefix='taxonomia')
            context['form_detalle'] = EspecieDetalleForm(self.request.POST, prefix='detalle')
        else:
            # Si es GET (primera carga), enviamos formularios vacíos
            context['form_taxonomia'] = TaxonomiaForm(prefix='taxonomia')
            context['form_detalle'] = EspecieDetalleForm(prefix='detalle')
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        form_taxonomia = context['form_taxonomia']
        form_detalle = context['form_detalle']

        if form.is_valid() and form_taxonomia.is_valid() and form_detalle.is_valid():
            with transaction.atomic():
                # Guardamos la Especie (Padre)
                self.object = form.save(commit=False)
                self.object.creador = self.request.user
                self.object.save()

                # Guardamos Taxonomía vinculándola a la especie creada
                taxonomia = form_taxonomia.save(commit=False)
                taxonomia.especie = self.object
                taxonomia.save()

                # Guardamos Detalle vinculándolo a la especie creada
                detalle = form_detalle.save(commit=False)
                detalle.especie = self.object
                detalle.save()

            return super().form_valid(form)
        else:
            # Si alguno falla, volvemos a renderizar la página con los errores
            return self.render_to_response(self.get_context_data(form=form))
    
# Editar Especie
class EspecieUpdateView(UpdateView, StaffRequireMixin):
    model = Especie
    form_class = EspecieForm
    template_name = "staff/especie_form.html"
    success_url = reverse_lazy('panel:mis_especies')        
    
    # Solo si el usuario es ADMIN o STAFF y creador de la especie
    def get_queryset(self):
        if self.request.user.rol == Usuario.Rol.ADMIN:
            return super().get_queryset()
        if self.request.user.rol == Usuario.Rol.STAFF:
            return Especie.objects.filter(creador=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            taxonomia_instance = self.object.taxonomia
        except ObjectDoesNotExist:
            taxonomia_instance = None

        try:
            detalle_instance = self.object.detalle
        except ObjectDoesNotExist:
            detalle_instance = None

        # 2. Inicializamos los formularios
        if self.request.POST:
            # En POST: pasamos la data (request.POST) Y la instancia para saber qué actualizar
            context['form_taxonomia'] = TaxonomiaForm(self.request.POST, instance=taxonomia_instance, prefix='taxonomia')
            context['form_detalle'] = EspecieDetalleForm(self.request.POST, instance=detalle_instance, prefix='detalle')
        else:
            # En GET: solo pasamos la instancia para que el form se pinte con los datos
            context['form_taxonomia'] = TaxonomiaForm(instance=taxonomia_instance, prefix='taxonomia')
            context['form_detalle'] = EspecieDetalleForm(instance=detalle_instance, prefix='detalle')
            
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form_taxonomia = context['form_taxonomia']
        form_detalle = context['form_detalle']

        if form.is_valid() and form_taxonomia.is_valid() and form_detalle.is_valid():
            with transaction.atomic():
                # 1. Guardamos la Especie (Padre)
                self.object = form.save()
                
                # 2. Guardamos Taxonomía
                taxonomia = form_taxonomia.save(commit=False)
                taxonomia.especie = self.object
                taxonomia.save()

                # 3. Guardamos Detalle
                detalle = form_detalle.save(commit=False)
                detalle.especie = self.object
                detalle.save()

            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

# Eliminar Curso
class EspecieDeleteView(DeleteView, StaffRequireMixin):
    model = Especie
    template_name = "staff/eliminar_especie.html"
    context_object_name = "especie"
    success_url = reverse_lazy('panel:mis_especies')
    
    # Solo si el usuario es ADMIN o STAFF y creador de la especie
    def get_queryset(self):
        if self.request.user.rol == Usuario.Rol.ADMIN:
            return super().get_queryset()
        if self.request.user.rol == Usuario.Rol.STAFF:
            return Especie.objects.filter(creador=self.request.user)
        
    def form_valid(self, form):
        especie = self.get_object()
        especie.soft_delete()
        return HttpResponseRedirect(self.get_success_url())