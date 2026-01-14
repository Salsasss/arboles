from django.db import models

from . import Especie

FUENTE_CHOICES = [
    ('Kew', 'Kew Gardens (POWO)'),
    ('IUCN', 'Lista Roja de Especies Amenazadas'),
    ('CONABIO', 'Enciclovida / CONABIO'),
    ('GBIF', 'Global Biodiversity Information Facility'),
    ('iNat', 'iNaturalista'),
    ('Wiki', 'Wikipedia'),
    ('Video', 'YouTube / Video'),
    ('Otro', 'Otra fuente'),
]

class Url(models.Model):
    especie = models.ForeignKey(
        Especie,
        on_delete=models.CASCADE,
        related_name='urls',  # Para acceder a las fotos -> especie.imagenes.all()
        verbose_name="Especie"
    )
    
    tipo = models.CharField(
        max_length=20,
        choices=FUENTE_CHOICES,
        default='Otro',
        verbose_name="Tipo de Fuente"
    )
    
    url = models.URLField(
        max_length=500, 
        verbose_name="Dirección Web (URL)"
    )
    
    class Meta:
        verbose_name = "URL"
        verbose_name_plural = "URLs"

    def __str__(self):
        return f"URL - {self.tipo}: {self.especie}"