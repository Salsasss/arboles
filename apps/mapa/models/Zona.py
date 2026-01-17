from django.db import models
from django.db.models import Sum
from django.utils.text import slugify

class Zona(models.Model):
    nombre = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Nombre de la Zona",
        help_text="Escribe el nombre simple."
    )
    
    descripcion = models.TextField(
        blank=True,
        verbose_name="Descripcion",
        help_text="Un nombre mas descriptivo.",
        )
    
    vector_path = models.TextField(help_text="El atributo 'd' del path SVG")

    slug = models.SlugField(
        max_length=255, 
        unique=True, 
        blank=True, # Vacio para que se autogenere
        help_text="Texto para la URL (se genera automáticamente si se deja vacío)."
    )
    
    def __str__(self):
        return f'{self.nombre} - {self.descripcion}'
    
    @property
    def total_arboles(self):
        """Devuelve la suma total de árboles en esta zona"""
        resultado = self.inventario.aggregate(total=Sum('cantidad'))
        return resultado['total'] or 0

    def top_especies(self, limite=5):
        """Devuelve las 5 especies más abundantes de esta zona"""
        # Usamos select_related para no matar la DB consultando nombres uno por uno
        return self.inventario.select_related('especie').order_by('-cantidad')[:limite]

    # Generar el slug automáticamente
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)