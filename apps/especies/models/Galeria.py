from django.db import models

import sys
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
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
    
    def save(self, *args, **kwargs):
        if self.imagen:
            img = Image.open(self.imagen)
            
            # Si no es WebP o es muy grande, procesamos
            if img.format != 'WEBP':
                output = BytesIO()
                
                # Convertimos a RGB si es necesario
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Guardamos como WebP
                img.save(output, format='WEBP', quality=80)
                output.seek(0)

                # Cambiamos el nombre del archivo a .webp
                nombre_nuevo = self.imagen.name.split('.')[0] + '.webp'
                
                # Reemplazamos el archivo en memoria
                self.imagen = InMemoryUploadedFile(
                    output, 
                    'ImageField', 
                    nombre_nuevo, 
                    'image/webp', 
                    sys.getsizeof(output), 
                    None
                )

        super().save(*args, **kwargs)