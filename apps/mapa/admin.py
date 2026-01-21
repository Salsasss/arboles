from django.contrib import admin

from apps.especies.models import Especie
from .models import Historial, Zona, Inventario

@admin.register(Historial)
class HistorialAdmin(admin.ModelAdmin):
    list_display = ('imagen', 'fecha_asociada', 'fecha_creacion', 'autor')
    list_filter = ('autor', )    
    search_fields = ('fecha_asociada', )
    ordering = ('fecha_creacion', )
    
class InventarioInline(admin.TabularInline):
    model = Inventario
    extra = 1
    autocomplete_fields = ['especie']
        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "especie":
            kwargs["queryset"] = Especie.all_objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Zona)
class ZonaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    exclude = ('slug', )
    inlines = [InventarioInline]
    
    # Sobrescribimos el método que gestiona el guardado de relaciones
    def save_related(self, request, form, formsets, change):
        # 1. Ejecuta el guardado normal primero (guarda la Zona y los inlines manuales)
        super().save_related(request, form, formsets, change)
        
        # 2. Obtenemos la instancia de la Zona que se acaba de guardar
        zona = form.instance
        
        # 3. Detectamos qué especies YA tienen registro en esta zona
        # (Usamos flat=True para tener una lista simple de IDs: [1, 5, 8...])
        ids_existentes = zona.inventario.values_list('especie_id', flat=True)
        
        # 4. Buscamos todas las especies que FALTAN
        especies_faltantes = Especie.all_objects.exclude(id__in=ids_existentes)
        
        # 5. Preparamos la creación masiva (Bulk Create es muy eficiente)
        nuevos_registros = []
        for especie in especies_faltantes:
            nuevos_registros.append(
                Inventario(zona=zona, especie=especie, cantidad=0)
            )
        
        # 6. Guardamos todo de golpe en la DB
        if nuevos_registros:
            Inventario.objects.bulk_create(nuevos_registros)
    
@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ['zona', 'especie', 'cantidad']
    list_filter = ('zona', 'especie')
    search_fields = ('especie__nombre_comun', 'especie__nombre_cientifico')
    ordering = ('-cantidad', )