from django.db import models

from apps.especies.models import Especie
from . import Zona

class Inventario(models.Model):
    zona = models.ForeignKey(
        Zona,
        on_delete=models.CASCADE,
        related_name='inventario',
        verbose_name="Zona Ubicación"
    )
    
    especie = models.ForeignKey(
        Especie,
        on_delete=models.CASCADE,
        related_name='ubicaciones',
        verbose_name="Especie"
    )
    
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        # Evitar duplicados: No puedes tener dos registros de "Roble" en "Zona A"
        unique_together = ('zona', 'especie')
        ordering = ['-cantidad']
        verbose_name_plural = "Inventario Forestal"

    def __str__(self):
        return f"{self.zona} - {self.especie}: {self.cantidad}"