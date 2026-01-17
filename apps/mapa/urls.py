from django.urls import path

from .views import HistorialListView, inventario

urlpatterns = [
    # Historial
    path('historial', HistorialListView.as_view(), name="historial"),
    path('inventario', inventario, name="inventario"),
]