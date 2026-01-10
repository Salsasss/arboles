import os
from django.db.models import Aggregate, Count

from .models import Especie

# Especie

TIPO_CHOICES = [
    ('ARBOL', 'Árbol'),
    ('PALMERA', 'Palmera'),
]

ESTADO_CONSERVACION_CHOICES = [
    ('NE', 'No Evaluado (NE)'),
    ('DD', 'Datos Insuficientes (DD)'),
    ('LC', 'Preocupación Menor (LC)'),
    ('NT', 'Casi Amenazado (NT)'),
    ('VU', 'Vulnerable (VU)'),
    ('EN', 'En Peligro (EN)'),
    ('CR', 'En Peligro Crítico (CR)'),
    ('EW', 'Extinto en Estado Silvestre (EW)'),
    ('EX', 'Extinto (EX)'),
]

# Galeria

CATEGORIAS_CHOICES = [
    ('GENERAL', 'Vista General'),
    ('CORTEZA', 'Corteza'),
    ('HOJAS', 'Hoja / Folíolo'),
    ('FLORES', 'Flor / Pétalos'),
    ('FRUTO', 'Fruto / Piña'),
    ('SEMILLA', 'Semilla'),
    ('OTRO', 'Otro'),
]

def ruta_galeria(instance, filename):
    # 1. Recuperamos la extensión original del archivo (ej: .jpg)
    base, extension = os.path.splitext(filename)
    
    Galeria = instance.__class__
    query = Galeria.objects.filter(especie=instance.especie, categoria=instance.categoria)
    total = query.count()
    
    img = f"{str(instance.categoria).lower()}_{total + 1}{extension}"
    
    return os.path.join('galeria', instance.especie.slug, img)