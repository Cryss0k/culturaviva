"""Perfil de usuario con campos complementarios (Pablo)."""
from django.conf import settings
from django.db import models

from .validators import validar_rut


class Perfil(models.Model):
    class Rol(models.TextChoices):
        CLIENTE = 'cliente', 'Cliente'
        BOLETERIA = 'boleteria', 'Personal de boletería'
        PRODUCTOR = 'productor', 'Productor'

    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil')
    rut = models.CharField(max_length=12, unique=True, validators=[validar_rut])
    telefono = models.CharField(max_length=15, blank=True)
    rol_institucional = models.CharField(max_length=12, choices=Rol.choices, default=Rol.CLIENTE)

    def __str__(self):
        return f'Perfil de {self.usuario}'
