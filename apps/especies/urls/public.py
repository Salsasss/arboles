from django.urls import path

from ..views import public

app_name = "public"

urlpatterns = [
    # Especies
    path('', public.EspecieListView.as_view(), name="catalogo_especies"),
    path('detalle/<slug:slug>', public.EspecieDetailView.as_view(), name="detalle_especie"),
    # Galeria
    path('galeria', public.GaleriaListView.as_view(), name="galeria"),
]