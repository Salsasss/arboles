"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from apps.perfiles.views.auth import redirect_home, CustomLoginView, RegisterCreateView, CustomPasswordChangeView, CustomPasswordResetView, CustomPasswordResetConfirmView, CustomPasswordResetDoneView, CustomPasswordResetCompleteView

urlpatterns = [
    path('', redirect_home, name="home"),
    path('admin/', admin.site.urls),
    path('especies/', include('apps.especies.urls.public')),
    path('historial/', include('apps.mapa.urls')),
    path('panel/', include('apps.especies.urls.panel')),
    # Registration
    path('login/', CustomLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('registrar/', RegisterCreateView.as_view(), name="registrar"),
    path('settings/password', CustomPasswordChangeView.as_view(), name="cambiar_password"),
    # ¿Olvidaste tu contraseña?
    path('reset_password/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset_password_sent/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # Panel de usuarios
    path('perfiles/', include('apps.perfiles.urls')),
    # Para que funcione CKEditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)