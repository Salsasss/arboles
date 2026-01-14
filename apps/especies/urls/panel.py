from django.urls import path

from ..views import panel

app_name = "panel"

urlpatterns = [
    # Especies
    path('', panel.EspecieListView.as_view(), name="mis_especies"),
    path('crear/', panel.EspecieCreateView.as_view(), name="crear_especie"),
    path('editar/<slug:slug>', panel.EspecieUpdateView.as_view(), name="editar_especie"),
    path('eliminar/<slug:slug>', panel.EspecieDeleteView.as_view(), name="eliminar_especie"),
    path('activar/<slug:slug>', panel.EspecieActivarView.as_view(), name="activar_especie"),
    # Galeria
    path('galeria', panel.GaleriaListView.as_view(), name="mi_galeria"),
    path('galeria/crear', panel.GaleriaCreateView.as_view(), name="crear_imagen"),
    path('galeria/editar/<int:pk>', panel.GaleriaUpdateView.as_view(), name="editar_imagen"),
    path('galeria/eliminar/<int:pk>', panel.GaleriaDeleteView.as_view(), name="eliminar_imagen"),
    # Urls
    path('urls/<slug:slug>', panel.UrlListView.as_view(), name="urls"),
    path('urls/<slug:slug>/crear', panel.UrlCreateView.as_view(), name="crear_url"),
    path('urls/<slug:slug>/editar/<int:pk>', panel.UrlUpdateView.as_view(), name="editar_url"),
    path('urls/<slug:slug>/eliminar/<int:pk>', panel.UrlDeleteView.as_view(), name="eliminar_url"),
]