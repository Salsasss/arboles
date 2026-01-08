from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    is_super = models.BooleanField(default=False) # Va a cambiar