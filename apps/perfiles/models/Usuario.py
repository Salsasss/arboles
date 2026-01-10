from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    class Rol(models.TextChoices):
        MIEMBRO = 'MIEMBRO', 'Miembro'
        STAFF = 'STAFF', 'Staff'
        ADMIN = 'ADMIN', 'Administrador'
    
    rol = models.CharField(
        max_length=10, 
        choices=Rol.choices, 
        default=Rol.MIEMBRO,
        verbose_name="Rol de Usuario"
    )
    
    def save(self, *args, **kwargs):
        if self.rol == self.Rol.ADMIN:
            self.is_staff = True
            self.is_superuser = True
        elif self.rol == self.Rol.STAFF:
            self.is_staff = True
            self.is_superuser = False
        else: # MIEMBRO
            self.is_staff = False
            self.is_superuser = False
            
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.username} - {self.get_rol_display()}"