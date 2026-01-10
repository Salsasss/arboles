from django.views.generic import ListView

from .models import Historial

# Listar Imágenes del Historial de la Masa Arborea
class HistorialListView(ListView):
    model = Historial
    template_name = "mapa/historial.html"
    context_object_name = "imagenes"
    
    def get_queryset(self):
        return Historial.objects.order_by('fecha_asociada')