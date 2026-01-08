from django.contrib import admin

from .models import Especie, EspecieDetalle, Taxonomia, Galeria, Url

class TaxonomiaInline(admin.StackedInline):
    model = Taxonomia
    extra = 1
    can_delete = False

class EspecieDetalleInline(admin.StackedInline):
    model = EspecieDetalle
    extra = 1
    can_delete = False
    
class UrlInline(admin.TabularInline):
    model = Url
    extra = 6
    can_delete = False

@admin.register(Especie)
class EspecieAdmin(admin.ModelAdmin):
    list_display = ('nombre_comun', 'nombre_cientifico', 'tipo', 'estado_conservacion', 'diametro_maximo', 'altura_maxima', 'slug')
    list_filter = ('tipo', 'estado_conservacion')
    search_fields = ('nombre_comun', 'nombre_cientifico')
    ordering = ('nombre_cientifico', )
    inlines = [TaxonomiaInline, EspecieDetalleInline, UrlInline]
    
@admin.register(EspecieDetalle)
class EspecieDetalleAdmin(admin.ModelAdmin):
    list_display = ('especie', 'corteza', 'hojas', 'flores', 'frutos', 'semillas')
    list_filter = ('especie', )
    search_fields = ('especie', )
    ordering = ('especie__nombre_cientifico', )
    
@admin.register(Taxonomia)
class TaxonomiaAdmin(admin.ModelAdmin):
    list_display = ('especie', 'reino', 'division', 'clase', 'subclase', 'orden', 'familia', 'genero')
    list_filter = ('especie', 'familia', 'genero')
    search_fields = ('especie', )
    ordering = ('especie__nombre_cientifico', )
            
@admin.register(Galeria)
class GaleriaAdmin(admin.ModelAdmin):
    list_display = ('especie', 'autor', 'imagen', 'titulo', 'tipo', 'fecha_creacion')
    list_filter = ('especie', 'autor', 'tipo')
    search_fields = ('titulo', )
    ordering = ('fecha_creacion', )
    
@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    list_display = ('especie', 'tipo', 'url')
    list_filter = ('especie', 'tipo')
    search_fields = ('especie', )