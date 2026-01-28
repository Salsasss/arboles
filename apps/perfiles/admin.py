from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'rol', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('username', )
    
    fieldsets = UserAdmin.fieldsets + (('Rol', {'fields': ('rol', )}), )
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {'fields': ('rol', )}), )