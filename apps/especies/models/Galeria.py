from django.db import models

from ..models import Especie
from ..utils import ruta_galeria
from apps.perfiles.models import Usuario

TIPO_CHOICES = [
    ('GENERAL', 'Vista General'),
    ('TRONCO', 'Tronco'),
    ('CORTEZA', 'Corteza'),
    ('HOJA', 'Hoja / Folíolo'),
    ('RAMAS', 'Ramas'),
    ('FOLLAJE', 'Follaje (Copa)'),
    ('FRUTO', 'Fruto / Piña'),
    ('SEMILLA', 'Semilla'),
    ('OTRO', 'Otro'),
]

class Galeria(models.Model):
    especie = models.ForeignKey(
        Especie,
        on_delete=models.CASCADE,
        related_name='imagenes',  # Para acceder a las fotos -> especie.imagenes.all()
        verbose_name="Especie Asociada"
    )
    
    autor = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='imagenes',
        verbose_name="Autor"
    )
    
    imagen = models.ImageField(
        upload_to=ruta_galeria,
        verbose_name="Fotografía",
        help_text="Sube una imagen de alta calidad."
    )
    
    titulo = models.CharField(
        max_length=255,
        verbose_name="Titulo de la Imagen",
        help_text="Nombra tu imagen.",
        blank=True
    )
    
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default='GENERAL',
        verbose_name="Categoría de la imagen"
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now=True
    )
    
    class Meta:
        verbose_name = "Galería"
        verbose_name_plural = "Galería"