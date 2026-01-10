from django.db import models

from apps.perfiles.models import Usuario
from ..utils import ruta_historial

class Historial(models.Model):
    imagen = models.ImageField(
        upload_to=ruta_historial,
        verbose_name="Imagen Satelital del Campus",
        help_text="Sube una imagen de alta calidad."
    )
    
    autor = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='historial',
        verbose_name="Autor"
    )
    
    fecha_asociada = models.DateField(
        verbose_name="Fecha Asociada a la Imagen",
        help_text="Introduce la fecha en que fue tomada."
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now=True
    )
    
    class Meta:
        verbose_name = "Historial"
        verbose_name_plural = "Historial"
        ordering = ['fecha_creacion']