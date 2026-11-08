"""Helpers de permisos (Pablo: tarea P4).

Uso en vistas de gestión (el orden de los decoradores importa):
    @login_required                  # anónimo -> login
    @user_passes_test(exige_staff)   # autenticado sin permiso -> 403
"""
from django.core.exceptions import PermissionDenied


def es_staff(user):
    """True si el usuario está autenticado y es personal (is_staff)."""
    return user.is_authenticated and user.is_staff


def exige_staff(user):
    """Como es_staff, pero lanza 403 si el usuario ya inició sesión y no tiene permiso."""
    if not es_staff(user):
        raise PermissionDenied
    return True
