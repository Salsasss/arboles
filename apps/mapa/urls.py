from django.urls import path

from .views import HistorialListView, mapa_inventario, inventario_completo, exportar_inventario_csv, ZonaDetailView

urlpatterns = [
    # Historial
    path('mapa_historial', HistorialListView.as_view(), name="mapa_historial"),
    # Inventario Forestal
    path('mapa_inventario', mapa_inventario, name="mapa_inventario"),
    path('inventario_completo', inventario_completo, name="inventario_completo"),
    path('zona_detalle/<slug:slug>', ZonaDetailView.as_view(), name="zona_detalle"),
    path('exportar_inventario/<slug:slug>', exportar_inventario_csv, name="exportar_inventario"),
]