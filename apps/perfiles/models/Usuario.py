from django.contrib.auth.models import AbstractUser, Group
from django.db import models
import uuid

class Usuario(AbstractUser):
    # Campo UUID
    id_publico = models.UUIDField(
        default=uuid.uuid4, 
        editable=False, 
        unique=True
    )
    
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
            self.is_staff = True # Puede entrar al admin panel
            self.is_superuser = False
        else: # MIEMBRO
            self.is_staff = False
            self.is_superuser = False
        
        # Guardamos el usuario
        super().save(*args, **kwargs)

        # Limpiamos grupos anteriores para evitar que sea staff Y Admin a la vez
        self.groups.clear() 

        if self.rol == self.Rol.ADMIN:
            grupo, _ = Group.objects.get_or_create(name='Administrador')
            self.groups.add(grupo)
        elif self.rol == self.Rol.STAFF:
            grupo, _ = Group.objects.get_or_create(name='Staff')
            self.groups.add(grupo)
        elif self.rol == self.Rol.MIEMBRO:
            grupo, _ = Group.objects.get_or_create(name='Miembro')
            self.groups.add(grupo)
        
    def __str__(self):
        return f"{self.username} - {self.get_rol_display()}"
    
    # No se elimina solo se desactiva el usuario
    def soft_delete(self):
        self.is_active = False
        self.save()
        
    def activar(self):
        self.is_active = True
        self.save()