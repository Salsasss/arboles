from django.db import models
from ckeditor.fields import RichTextField

from . import Especie

class EspecieDetalle(models.Model):
    especie = models.OneToOneField(
        Especie,
        on_delete=models.CASCADE,
        primary_key=True, # La ID de este detalle será la misma ID de la especie
        related_name='detalle', # Para acceder desde la especie: especie.detalle.corteza
        verbose_name="Especie Asociada"
    )
    
    corteza = RichTextField(
        verbose_name="Descripción de la Corteza",
        help_text="Detalles sobre textura, color, grosor y desprendimiento.",
        blank=True,
        null=True
    )

    hojas = RichTextField(
        verbose_name="Descripción de las Hojas (Follaje)",
        help_text="Forma, borde, disposición, color y caducidad.",
        blank=True,
        null=True
    )

    flores = RichTextField(
        verbose_name="Descripción de las Flores",
        help_text="Color, tamaño, inflorescencia, época de floración y sexualidad.",
        blank=True,
        null=True
    )

    frutos = RichTextField(
        verbose_name="Descripción de los Frutos",
        help_text="Tipo de fruto, dimensiones, color al madurar y época de fructificación.",
        blank=True,
        null=True
    )

    semillas = RichTextField(
        verbose_name="Descripción de las Semillas",
        help_text="Forma, tamaño, método de dispersión y cultivo.",
        blank=True,
        null=True
    )
    
    biogeografia = RichTextField(
        verbose_name="Descripción de la Biogeografía",
        help_text="Origen, distribución, hábitat y condiciones ambientales",
        blank=True,
        null=True
    )
    
    importancia = RichTextField(
        verbose_name="Descripción de la Importancia",
        help_text="Usos, importancia cultural y económica.",
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = "Detalle Botánico"
        verbose_name_plural = "Detalles Botánicos"
        
    def __str__(self):
        return f"Detalles de: {self.especie}"