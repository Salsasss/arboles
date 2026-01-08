import os

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

def ruta_galeria(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.tipo}_{filename}"
    return os.path.join('galeria', instance.especie.slug, filename)