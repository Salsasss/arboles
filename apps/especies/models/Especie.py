from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify

from apps.perfiles.models import Usuario

TIPO_CHOICES = [
    ('ARBOL', 'Árbol'),
    ('PALMERA', 'Palmera'),
]

ESTADO_CONSERVACION_CHOICES = [
    ('NE', 'No Evaluado (NE)'),
    ('DD', 'Datos Insuficientes (DD)'),
    ('LC', 'Preocupación Menor (LC)'),
    ('NT', 'Casi Amenazado (NT)'),
    ('VU', 'Vulnerable (VU)'),
    ('EN', 'En Peligro (EN)'),
    ('CR', 'En Peligro Crítico (CR)'),
    ('EW', 'Extinto en Estado Silvestre (EW)'),
    ('EX', 'Extinto (EX)'),
]

class EspecieManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class Especie(models.Model):
    nombre_comun = models.CharField(
        max_length=150,
        db_index=True, # Opimizado para consultas en la DB
        verbose_name="Nombre Común",
        help_text="Nombre con el que se le conoce localmente."
    )
    
    nombre_cientifico = models.CharField(
        max_length=150,
        unique=True, # No debe haber dos especies con el mismo nombre cientifico
        db_index=True,
        verbose_name="Nombre Científico",
        help_text="Ej. Jatropha curcas"
    )
    
    tipo = models.CharField(
        max_length=10,
        choices=TIPO_CHOICES,
        default='ARBOL',
        verbose_name="Tipo de Especie"
    )
    
    estado_conservacion = models.CharField(
        max_length=3,
        choices=ESTADO_CONSERVACION_CHOICES,
        default='NE',
        verbose_name="Estado de Conservación (IUCN)"
    )

    diametro_maximo = models.DecimalField(
        max_digits=5, # Permite hasta 999.99
        decimal_places=2,
        verbose_name="Diámetro Máximo (cm)",
        help_text="Diámetro del tronco (DAP) promedio en centímetros.",
        blank=True,
        null=True
    )
    
    altura_maxima = models.DecimalField(
        max_digits=4, # Permite hasta 99.99 metros (suficiente para árboles)
        decimal_places=2,
        verbose_name="Altura Máxima (m)",
        help_text="Altura promedio que puede alcanzar en metros.",
        blank=True,
        null=True
    )
    
    descripcion = RichTextUploadingField(
        verbose_name="Descripción Completa",
        help_text="Permite formato de texto",
        config_name='default',
        blank=True
    )
    
    slug = models.SlugField(
        max_length=255, 
        unique=True, 
        blank=True, # Vacio para que se autogenere
        help_text="Texto para la URL (se genera automáticamente si se deja vacío)."
    )
    
    creador = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='especies',
        verbose_name="Autor"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activa",
    )
    
    objects = EspecieManager() # Solo entrega Especies activas -> Respeta el EspecieManager
    all_objects = models.Manager() # Entrega Especies activas e inactivas
    
    class Meta:
        verbose_name = "Especie"
        verbose_name_plural = "Especies"
        ordering = ['nombre_cientifico']
                
    def __str__(self):
        return f'{self.nombre_cientifico} - {self.nombre_comun}'
    
    # Generar el slug automáticamente
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre_cientifico)
        super().save(*args, **kwargs)
    
    # No se elimina solo se desactiva la especie
    def soft_delete(self):
        self.is_active = False
        self.save()