"""Vistas de autenticación (Pablo: tareas P2, P3). Por ahora son stubs."""
from django.http import HttpResponse


def _stub(nombre):
    return HttpResponse(f'Pendiente de implementar: {nombre} (Pablo)')


def registro(request):
    return _stub('cuentas:registro')


def login_vista(request):
    return _stub('cuentas:login')


def logout_vista(request):
    return _stub('cuentas:logout (POST)')


def perfil(request):
    return _stub('cuentas:perfil (login_required)')
