"""Validadores reutilizables del catálogo (Cristian)."""
import re

from django.core.exceptions import ValidationError

PATRON_CODIGO = re.compile(r'^[A-Z]{3}-\d{3}$')


def validar_codigo(valor):
    """El código debe tener el formato XXX-000 (ej: TEA-001)."""
    if not PATRON_CODIGO.match(valor):
        raise ValidationError('El código debe tener el formato XXX-000 (ej: TEA-001).')
