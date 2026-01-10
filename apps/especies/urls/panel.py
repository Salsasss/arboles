from django.urls import path

from ..views import panel

app_name = "panel"

urlpatterns = [
    # Especies
    path('', panel.EspecieListView.as_view(), name="mis_especies"),
    path('crear/', panel.EspecieCreateView.as_view(), name="crear_especie"),
    path('editar/<slug:slug>', panel.EspecieUpdateView.as_view(), name="editar_especie"),
    path('eliminar/<slug:slug>', panel.EspecieDeleteView.as_view(), name="eliminar_especie"),
]