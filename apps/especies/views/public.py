from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q

from ..models import Especie, Galeria
from ..utils import TIPO_CHOICES, ESTADO_CONSERVACION_CHOICES

# Listar Especies
class EspecieListView(ListView):
    model = Especie
    template_name = "especies/catalogo_especies.html"
    context_object_name = "especies"
    paginate_by = 8
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
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
    
    # Regresando el query para que se autocomplete en el buscador
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

# Detalle Especie
class EspecieDetailView(DetailView):
    model = Especie
    template_name = "especies/n.html"
    context_object_name = "especie"
    
    def get_queryset(self): # OJO en el futiuro quizas solo enviar imagen general, tronco, hoja, corteza, etc
        queryset = super().get_queryset()
        return queryset.select_related( # select_related -> 1:1
            'detalle',
            'taxonomia',
        ).prefetch_related('imagenes') # prefetch_related -> 1:N

# Listar Galeria
class GaleriaListView(ListView):
    model = Galeria
    template_name = "especies/s.html"
    context_object_name = "imagenes"
    paginate_by = 16
    
    def get_queryset(self):
        queryset = super().get_queryset()
                
        self.query = self.request.GET.get('query', '') # Buscador
        self.tipo = self.request.GET.get('tipo', '') # Filtro Tipo (Arbol, Palmera)
        self.estado = self.request.GET.get('estado', '') # Filtro IUCN (NE, DD, LC, NT, ...)

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
            
        return queryset
    
    # Regresando el query para que se autocomplete en el buscador
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

# Detalle Galeria
class GaleriaDetalleListView(ListView):
    model = Galeria
    template_name = "especies/detalle_galeria.html"
    context_object_name = "imagenes"
    paginate_by = 8
    
    def get_queryset(self):
        especie = get_object_or_404(Especie, slug=self.kwargs['slug'])
        return especie.imagenes.all().order_by('tipo')