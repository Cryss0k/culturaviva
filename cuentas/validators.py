"""Validadores de la app cuentas (Pablo)."""
import re

from django.core.exceptions import ValidationError


def limpiar_rut(valor):
    """Quita puntos, guiones y espacios; deja el RUT en mayúsculas."""
    return re.sub(r'[.\-\s]', '', valor or '').upper()


def normalizar_rut(valor):
    """Devuelve el RUT en formato 12345678-5 (sin puntos)."""
    limpio = limpiar_rut(valor)
    return f'{limpio[:-1]}-{limpio[-1]}' if len(limpio) > 1 else limpio


def validar_rut(valor):
    """Valida el RUT chileno con el algoritmo módulo 11."""
    limpio = limpiar_rut(valor)
    if not re.fullmatch(r'\d{7,8}[\dK]', limpio):
        raise ValidationError('Ingresa un RUT válido (ej: 12.345.678-5).')
    cuerpo, dv = limpio[:-1], limpio[-1]
    suma, multiplicador = 0, 2
    for digito in reversed(cuerpo):
        suma += int(digito) * multiplicador
        multiplicador = 2 if multiplicador == 7 else multiplicador + 1
    resto = 11 - suma % 11
    esperado = 'K' if resto == 10 else '0' if resto == 11 else str(resto)
    if dv != esperado:
        raise ValidationError('El RUT no es válido (dígito verificador incorrecto).')
