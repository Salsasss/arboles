from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from django.db.models import OuterRef, Subquery
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.db import transaction

from ..models import Especie, Galeria, Url
from ..forms import EspecieForm, TaxonomiaForm, EspecieDetalleForm, GaleriaForm, UrlForm
from ..utils import TIPO_CHOICES, CATEGORIAS_CHOICES, ESTADO_CONSERVACION_CHOICES, ESTADO_ESPECIE

from apps.perfiles.models import Usuario

class StaffRequireMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.rol == Usuario.Rol.STAFF or self.request.user.rol == Usuario.Rol.ADMIN
    
# Listar Especies
class EspecieListView(StaffRequireMixin, ListView):
    model = Especie
    template_name = "staff/mis_especies.html"
    context_object_name = "especies"
    paginate_by = 12
    
    def get_queryset(self):
        queryset = self.model.all_objects.get_queryset() # Trae todas las especies incluso las inactivas
        queryset = queryset.prefetch_related(
            Prefetch(
                'imagenes',
                queryset=Galeria.all_objects.all(), # Traera todas las imagenes incluso las de especies inactivas
            )
        )
        
        # Solo muestra las especies que yo cree
        if self.request.user.rol == Usuario.Rol.STAFF:
            queryset = queryset.filter(creador=self.request.user)
        
        self.query = self.request.GET.get('query', '') # Buscador
        self.tipo = self.request.GET.get('tipo', '') # Filtro tipo (Arbol, Palmera)
        self.estado = self.request.GET.get('estado', '') # Filtro estado IUCN (NE, DD, LC, NT, ...)
        self.estado_especie = self.request.GET.get('estado_especie', '') # Filtro estado (Activa, Inactiva)
        
        # Buscador
        if self.query:            
            queryset = queryset.filter(
                Q(nombre_comun__icontains=self.query) |
                Q(nombre_cientifico__icontains=self.query) |
                Q(taxonomia__familia__icontains=self.query) |
                Q(taxonomia__genero__icontains=self.query)
            )
            
        # Filtros
        if self.tipo:
            queryset = queryset.filter(tipo=self.tipo)
            
        if self.estado:
            queryset = queryset.filter(estado_conservacion=self.estado)
    
        if self.estado_especie:
            queryset = queryset.filter(is_active=self.estado_especie)
    
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Buscador
        context['query'] = self.query
        
        # Filtros|
        context['TIPO_CHOICES'] = TIPO_CHOICES
        context['ESTADO_CONSERVACION_CHOICES'] = ESTADO_CONSERVACION_CHOICES
        context['ESTADO_ESPECIE'] = ESTADO_ESPECIE
        context['tipo'] = self.tipo
        context['estado'] = self.estado
        context['estado_especie'] = self.estado_especie
        
        return context
    
# Crear Especie
class EspecieCreateView(StaffRequireMixin, CreateView):
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
class EspecieUpdateView(StaffRequireMixin, UpdateView):
    model = Especie
    form_class = EspecieForm
    template_name = "staff/especie_form.html"
    success_url = reverse_lazy('panel:mis_especies')        
    
    # Solo si el usuario es ADMIN o STAFF y creador de la especie
    def get_queryset(self):
        queryset = self.model.all_objects.get_queryset()
        if self.request.user.rol == Usuario.Rol.ADMIN:
            return queryset
        if self.request.user.rol == Usuario.Rol.STAFF:
            return queryset.filter(creador=self.request.user)
        return queryset.none() # Si no es ni ADMIN ni STAFF
    
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

# Eliminar Especie
class EspecieDeleteView(StaffRequireMixin, DeleteView):
    model = Especie
    template_name = "eliminar_objeto.html"
    context_object_name = "especie"
    success_url = reverse_lazy('panel:mis_especies')
    
    # Solo si el usuario es ADMIN o STAFF y creador de la especie
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.rol == Usuario.Rol.ADMIN:
            return queryset
        if self.request.user.rol == Usuario.Rol.STAFF:
            return queryset.filter(creador=self.request.user)
        return queryset.none() # Si no es ni ADMIN ni STAFF
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clase'] = "Especie"
        context['accion'] = "Desactivar"
        context['success_url'] = reverse_lazy('panel:mis_especies')
        return context
        
    def form_valid(self, form):
        especie = self.get_object()
        especie.soft_delete()
        return HttpResponseRedirect(self.get_success_url())
    
# Activar Especie
class EspecieActivarView(StaffRequireMixin, UpdateView):
    model = Especie
    fields = []
    template_name = "activar_objeto.html"
    success_url = reverse_lazy('panel:mis_especies')
    
    # Solo si el usuario es ADMIN o STAFF y creador de la especie
    def get_queryset(self):
        queryset = self.model.all_objects.get_queryset() # Tiene que ser este metodo para que traiga todos, inclusive los Inactivos
        if self.request.user.rol == Usuario.Rol.ADMIN:
            return queryset
        if self.request.user.rol == Usuario.Rol.STAFF:
            return queryset.filter(creador=self.request.user)
        return queryset.none() # Si no es ni ADMIN ni STAFF
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clase'] = "Especie"
        context['success_url'] = reverse_lazy('panel:mis_especies')
        return context
    
    def form_valid(self, form):
        self.object.activar()
        return super().form_valid(form)
    
# Listar Imagenes
class GaleriaListView(StaffRequireMixin, ListView):
    model = Galeria
    template_name = "staff/mi_galeria.html"
    context_object_name = "imagenes"
    paginate_by = 16
    
    def get_queryset(self):
        subquery = Galeria.all_objects.filter(
            especie=OuterRef('especie'), # Valor de afuera
            categoria='GENERAL'
        ).values('imagen')[:1]
        
        queryset = self.model.all_objects.get_queryset().select_related('especie').annotate(
            imagen_principal=Subquery(subquery)
        )
        
        # Solo muestra las imagenes que yo subí
        if self.request.user.rol == Usuario.Rol.STAFF:
            queryset = queryset.filter(autor=self.request.user)
                
        self.query = self.request.GET.get('query', '') # Buscador
        self.tipo = self.request.GET.get('tipo', '') # Filtro Tipo (Arbol, Palmera)
        self.estado = self.request.GET.get('estado', '') # Filtro IUCN (NE, DD, LC, NT, ...)
        self.especie_buscar = self.request.GET.get('especie_buscar', '') # Filtro Especie
        self.categoria = self.request.GET.get('categoria', '') # Filtro Categoria Imagen
        
        # Para eficiencia mejora los JOINS
        queryset = queryset.select_related('especie', 'especie__taxonomia') 
        
        # Buscador
        if self.query:
            queryset = queryset.filter(
                Q(especie__nombre_comun__icontains=self.query) |
                Q(especie__nombre_cientifico__icontains=self.query) |
                Q(especie__taxonomia__familia__icontains=self.query) |
                Q(especie__taxonomia__genero__icontains=self.query)
            )
    
        #Filtros
        if self.tipo:
            queryset = queryset.filter(especie__tipo=self.tipo)
            
        if self.estado:
            queryset = queryset.filter(especie__estado_conservacion=self.estado)
            
        if self.especie_buscar:
            self.especie_buscar = int(self.especie_buscar)
            queryset = queryset.filter(especie=self.especie_buscar)
        
        if self.categoria:
            queryset = queryset.filter(categoria=self.categoria)
            
        return queryset
    
    # Regresando el query para que se autocomplete en el buscador
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Buscador
        context['query'] = self.query
        
        # Filtros
        context['TIPO_CHOICES'] = TIPO_CHOICES
        context['ESPECIE_BUSCAR_CHOICES'] = Especie.all_objects.values_list('id', 'nombre_comun').order_by('nombre_comun') # Hacemos la consulta al momento para que no se desactualize
        context['ESTADO_CONSERVACION_CHOICES'] = ESTADO_CONSERVACION_CHOICES
        context['CATEGORIAS_CHOICES'] = CATEGORIAS_CHOICES
        
        # Para preecargar los valores
        context['tipo'] = self.tipo
        context['estado'] = self.estado
        context['especie_buscar'] = self.especie_buscar
        context['categoria'] = self.categoria
        return context

# Crear Imagen
class GaleriaCreateView(StaffRequireMixin, CreateView):
    model = Galeria
    form_class = GaleriaForm
    template_name = "staff/imagen_form.html"
    success_url = reverse_lazy('panel:mi_galeria')
    
    def form_valid(self, form):
        if form.is_valid():
            # Guardamos el autor
            self.object = form.save(commit=False)
            self.object.autor = self.request.user
            self.object.save()
            
            return super().form_valid(form)
        else:
            # Si alguno falla, volvemos a renderizar la página con los errores
            return self.render_to_response(self.get_context_data(form=form))

# Editar Imagen
class GaleriaUpdateView(StaffRequireMixin, UpdateView):
    model = Galeria
    form_class = GaleriaForm
    template_name = "staff/imagen_form.html"
    success_url = reverse_lazy('panel:mi_galeria')
    
    def get_queryset(self):
        queryset = self.model.all_objects.get_queryset()
        if self.request.user.rol == Usuario.Rol.ADMIN:
            return queryset
        if self.request.user.rol == Usuario.Rol.STAFF:
            return queryset.filter(autor=self.request.user)
        return queryset.none() # Si no es ni ADMIN ni STAFF
    
# Eliminar Imagen
class GaleriaDeleteView(StaffRequireMixin, DeleteView):
    model = Galeria
    template_name = "eliminar_objeto.html"
    success_url = reverse_lazy('panel:mi_galeria')
    
    # Solo si el usuario es ADMIN o STAFF y autor de la Imagen
    def get_queryset(self):
        queryset = self.model.all_objects.get_queryset()
        if self.request.user.rol == Usuario.Rol.ADMIN:
            return queryset
        if self.request.user.rol == Usuario.Rol.STAFF:
            return queryset.filter(autor=self.request.user)
        return queryset.none() # Si no es ni ADMIN ni STAFF
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clase'] = "Imagen"
        context['accion'] = "Eliminar"
        context['success_url'] = reverse_lazy('panel:mi_galeria')
        return context

# Listar URLs
class UrlListView(StaffRequireMixin, ListView):
    model = Url
    template_name = "staff/urls.html"
    context_object_name = "urls"
    
    def get_queryset(self):
        self.especie = get_object_or_404(Especie.all_objects, slug=self.kwargs['slug'])
        return self.especie.urls.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['especie'] = self.especie
        return context

# Crear URL
class UrlCreateView(StaffRequireMixin, CreateView):
    model = Url
    form_class = UrlForm
    template_name = "staff/url_form.html"
    
    def form_valid(self, form):
        especie = get_object_or_404(Especie.all_objects, slug=self.kwargs['slug'])
        
        if form.is_valid():
            # Guardamos el autor
            self.object = form.save(commit=False)
            self.object.especie = especie
            self.object.save()
            
            return super().form_valid(form)
        else:
            # Si alguno falla, volvemos a renderizar la página con los errores
            return self.render_to_response(self.get_context_data(form=form))
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        return context
        
    def get_success_url(self):
        return reverse_lazy('panel:urls', args=[self.kwargs['slug']])

# Editar URL
class UrlUpdateView(StaffRequireMixin, UpdateView):
    model = Url
    form_class = UrlForm
    template_name = "staff/url_form.html"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.rol == Usuario.Rol.ADMIN:
            return queryset
        if self.request.user.rol == Usuario.Rol.STAFF:
            return queryset.filter(especie__creador=self.request.user)
        return queryset.none() # Si no es ni ADMIN ni STAFF
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        return context
    
    def get_success_url(self):
        return reverse_lazy('panel:urls', args=[self.kwargs['slug']])

# Eliminar URL
class UrlDeleteView(StaffRequireMixin, DeleteView):
    model = Url
    template_name = "eliminar_objeto.html"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.rol == Usuario.Rol.ADMIN:
            return queryset
        if self.request.user.rol == Usuario.Rol.STAFF:
            return queryset.filter(especie__creador=self.request.user)
        return queryset.none()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clase'] = "URL"
        context['accion'] = "Eliminar"
        context['success_url'] = self.get_success_url()
        return context
    
    def get_success_url(self):
        return reverse_lazy('panel:urls', args=[self.kwargs['slug']])