import os

from .models import Historial

def ruta_historial(instance, filename):
    base, extension = os.path.splitext(filename)
    
    Historial = instance.__class__
    
    total = Historial.objects.count()
    
    img = f'historial_{total + 1}{extension}'
    return os.path.join('historial', img)