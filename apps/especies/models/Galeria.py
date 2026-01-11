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
    
    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIAS_CHOICES,
        default='GENERAL',
        verbose_name="Categoría de la imagen"
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now=True
    )
    
    objects = GaleriaManager() # Solo entrega imagenes de Especies activas -> Respeta el GaleriaManager
    all_objects = models.Manager() # Entrega imagenes de Especies activas e inactivas
    
    class Meta:
        verbose_name = "Galería"
        verbose_name_plural = "Galería"
        
    def __str__(self):
        return f'{self.categoria} de {self.especie}'