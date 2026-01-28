import csv
import codecs
from django.db.models import Sum
from django.db.models import OuterRef, Subquery
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.shortcuts import render

from apps.especies.models import Especie, Galeria
from .models import Historial, Zona

# Listar Imágenes del Historial de la Masa Forestal
class HistorialListView(ListView):
    model = Historial
    template_name = "mapa/mapa_historial.html"
    context_object_name = "imagenes"
    
def mapa_inventario(request):
    return render(request, "mapa/mapa_inventario.html", {
        'zonas': Zona.objects.all()
    })

def inventario_completo(request):
    subquery = Galeria.all_objects.filter(
        especie_id=OuterRef('id'), # Valor de afuera
        categoria='GENERAL'
    ).values('imagen')[:1]
    
    inventario = Especie.all_objects.annotate(
        cantidad=Sum('inventario__cantidad'),
        imagen_principal=Subquery(subquery)
    ).order_by('-cantidad')

    # Para compatibilidad del template
    # El template espera {{ item.especie }} -> Hacemos que el objeto item se apunte a sí mismo.
    
    for item in inventario:
        item.especie = item
    
    zona = Zona.objects.get(slug="campus")
    zona.total_arboles = inventario.aggregate(total=Sum('cantidad'))['total']
    zona.top_especies = inventario.order_by('-cantidad')[:5]
    
    for item in zona.top_especies:
        item.especie = item
    
    return render(request, "mapa/zona_detalle.html", {
        'zona': zona,
        'dominante': inventario.first,
        'inventario': inventario
    })

def exportar_inventario_csv(request, slug):
    zona = get_object_or_404(Zona, slug=slug)
    
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="inventario_zona_{zona.slug}.csv"'
    response.write(codecs.BOM_UTF8)

    writer = csv.writer(response)
    writer.writerow(['Nombre Común', 'Nombre Científico', 'Cantidad'])

    if slug == "campus":
        inventario = Especie.all_objects.annotate(
            cantidad=Sum('inventario__cantidad')
        ).order_by('-cantidad')
        
        for item in inventario:
            item.especie = item
    else:
        inventario = zona.inventario.filter(cantidad__gt=0).select_related('especie')

    for registro in inventario:
        writer.writerow([
            registro.especie.nombre_comun,
            registro.especie.nombre_cientifico,
            registro.cantidad,
        ])

    return response

# Detalle de la Zona
class ZonaDetailView(DetailView):
    model = Zona
    template_name = "mapa/zona_detalle.html"
    context_object_name = "zona"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['dominante'] = self.object.inventario.first # Esta ordenado -> First es el mas abundante
        
        subquery = Galeria.all_objects.filter(
            especie=OuterRef('especie'), # Valor de afuera
            categoria='GENERAL'
        ).values('imagen')[:1]

        context['inventario'] = self.object.inventario.filter(
            cantidad__gt=0
        ).select_related('especie').annotate(
            imagen_principal=Subquery(subquery)
        ).order_by('-cantidad')
        
        return context