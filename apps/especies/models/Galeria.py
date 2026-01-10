from django.db import models

from ..models import Especie
from ..utils import ruta_galeria, CATEGORIAS_CHOICES
from apps.perfiles.models import Usuario

class GaleriaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(especie__is_active=True)

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
    
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIAS_CHOICES,
        default='GENERAL',
        verbose_name="Categoría de la imagen"
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now=True
    )
    
    # Para que solo entrege las imagenes de especies activas
    objects = GaleriaManager()
    all_objects = models.Manager()
    
    class Meta:
        verbose_name = "Galería"
        verbose_name_plural = "Galería"