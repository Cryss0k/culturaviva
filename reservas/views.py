"""Vistas del carrito (Cristian: tarea C8). Por ahora son stubs."""
from django.http import HttpResponse


def _stub(nombre):
    return HttpResponse(f'Pendiente de implementar: {nombre} (Cristian)')


def ver(request):
    return _stub('reservas:ver')


def agregar(request, espectaculo_id):
    return _stub('reservas:agregar (POST)')


def modificar(request, espectaculo_id):
    return _stub('reservas:modificar (POST)')


def eliminar(request, espectaculo_id):
    return _stub('reservas:eliminar (POST)')


def vaciar(request):
    return _stub('reservas:vaciar (POST)')


def confirmar(request):
    return _stub('reservas:confirmar (POST, login_required)')


def comprobante(request):
    return _stub('reservas:comprobante (login_required)')
