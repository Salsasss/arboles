from django.views.generic import ListView
from django.shortcuts import render
from .models import Historial

# Listar Imágenes del Historial de la Masa Forestal
class HistorialListView(ListView):
    model = Historial
    template_name = "mapa/historial.html"
    context_object_name = "imagenes"
    
    def get_queryset(self):
        return Historial.objects.order_by('fecha_asociada')
    
def inventario(request):
    return render(request, "mapa/inventario.html")