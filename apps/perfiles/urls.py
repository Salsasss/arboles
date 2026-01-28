from django.urls import path

from .views.user import UsuarioListView, UsuarioCreateView, UsuarioUpdateView, UsuarioDeleteView, UsuarioActivarView

urlpatterns = [
    path('panel', UsuarioListView.as_view(), name='panel'),
    path('panel/crear', UsuarioCreateView.as_view(), name='crear_usuario'),
    path('panel/editar/<uuid:id_publico>', UsuarioUpdateView.as_view(), name='editar_usuario'),
    path('panel/eliminar/<uuid:id_publico>', UsuarioDeleteView.as_view(), name='eliminar_usuario'),
    path('panel/activar/<uuid:id_publico>', UsuarioActivarView.as_view(), name='activar_usuario'),
]