from django.urls import path

from .views import HistorialListView

urlpatterns = [
    # Historial
    path('historial', HistorialListView.as_view(), name="historial"),
]