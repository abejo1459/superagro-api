from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLES = (
        ('ADMIN', 'Administrador'),
        ('VENDEDOR', 'Vendedor'),
        ('ALMACENISTA', 'Almacenista'),
    )
    
    cedula = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255)
    rol = models.CharField(max_length=20, choices=ROLES, default='VENDEDOR')

    def __str__(self):
        return f"{self.username} - {self.get_rol_display()}"
