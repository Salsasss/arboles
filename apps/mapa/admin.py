from django.contrib import admin

from .models import Historial

@admin.register(Historial)
class HistorialAdmin(admin.ModelAdmin):
    list_display = ('imagen', 'fecha_asociada', 'fecha_creacion', 'autor')
    list_filter = ('autor', )    
    search_fields = ('fecha_asociada', )
    ordering = ('fecha_creacion', )