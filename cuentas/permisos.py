"""Helpers de permisos (Pablo: tarea P4).

Uso en vistas de gestión:
    @login_required
    @user_passes_test(es_staff)
"""


def es_staff(user):
    return user.is_authenticated and user.is_staff
