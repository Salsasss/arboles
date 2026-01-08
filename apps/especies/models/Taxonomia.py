from django.db import models

from . import Especie

class Taxonomia(models.Model):
    especie = models.OneToOneField(
        Especie,
        on_delete=models.CASCADE,
        primary_key=True, # La ID de este detalle será la misma ID de la especie
        related_name='taxonomia', # Para acceder desde la especie: especie.taxonomia.reino
        verbose_name="Especie Asociada"
    )
    
    reino = models.CharField(
        max_length=50,
        default="Plantae", # Casi siempre será "Plantae", podemos ponerlo por defecto
        verbose_name="Reino"
    )

    # Equivalente a Phylum en botánica
    division = models.CharField(
        max_length=100,
        verbose_name="División",
        help_text="Ej. Streptophyta"
    )

    clase = models.CharField(
        max_length=100,
        verbose_name="Clase",
        help_text="Ej. Equisetopsida"
    )

    # No siempre se usa en todas las clasificaciones, se dejará opcional
    subclase = models.CharField(
        max_length=100,
        verbose_name="Subclase",
        help_text="Ej. Magnoliidae",
        blank=True,
        null=True
    )

    orden = models.CharField(
        max_length=100,
        verbose_name="Orden",
        help_text="Ej. Sapindales"
    )

    familia = models.CharField(
        max_length=100,
        verbose_name="Familia",
        db_index=True, # Optimizado para consultas en la DB
        help_text="Ej. Burseraceae"
    )

    genero = models.CharField(
        max_length=100,
        verbose_name="Género",
        db_index=True,
        help_text="Ej. Bursera"
    )

    class Meta:
        verbose_name = "Clasificación Taxonómica"
        verbose_name_plural = "Clasificaciones Taxonómicas"

    def __str__(self):
        return f"Taxonomía de {self.especie}"