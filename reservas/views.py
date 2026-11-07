"""Vistas del carrito de entradas y del comprobante (Cristian: tarea C8)."""
import secrets

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .carrito import SESSION_COMPROBANTE, Carrito


def _notificar(request, resultado):
    """Muestra (ok, mensaje) con el framework de mensajes."""
    ok, mensaje = resultado
    (messages.success if ok else messages.error)(request, mensaje)


def _destino_seguro(request, por_defecto):
    """Usa el parámetro 'next' solo si apunta a este mismo sitio (evita open redirect)."""
    destino = request.POST.get('next', '')
    if destino and url_has_allowed_host_and_scheme(
            destino, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        return destino
    return reverse(por_defecto)


def ver(request):
    """Muestra el carrito con el desglose de subtotal, recargo, IVA y total."""
    carrito = Carrito(request)
    items = carrito.items()
    contexto = {
        'items': items,
        'resumen': carrito.resumen(items),
        'hay_errores': any(item['error'] for item in items),
        'max_entradas': settings.MAX_ENTRADAS_POR_COMPRA,
        'recargo_pct': int(settings.RECARGO_SERVICIO_PORCENTAJE * 100),
        'iva_pct': int(settings.IVA_PORCENTAJE * 100),
    }
    return render(request, 'reservas/carrito.html', contexto)


@require_POST
def agregar(request, espectaculo_id):
    _notificar(request, Carrito(request).agregar(espectaculo_id, request.POST.get('cantidad', 1)))
    return redirect(_destino_seguro(request, 'reservas:ver'))


@require_POST
def modificar(request, espectaculo_id):
    _notificar(request, Carrito(request).modificar(espectaculo_id, request.POST.get('cantidad')))
    return redirect('reservas:ver')


@require_POST
def eliminar(request, espectaculo_id):
    _notificar(request, Carrito(request).eliminar(espectaculo_id))
    return redirect('reservas:ver')


@require_POST
def vaciar(request):
    Carrito(request).vaciar()
    messages.success(request, 'Vaciaste tu carrito.')
    return redirect('reservas:ver')


@login_required
@require_POST
def confirmar(request):
    """Valida el carrito, genera un comprobante simulado y vacía la sesión.

    No persiste nada en la base de datos ni descuenta stock (solicitud simulada).
    """
    carrito = Carrito(request)
    items = carrito.items()
    errores = carrito.validar(items)
    if errores:
        for error in errores:
            messages.error(request, error)
        return redirect('reservas:ver')

    resumen = carrito.resumen(items)
    ahora = timezone.localtime()
    request.session[SESSION_COMPROBANTE] = {
        'codigo': f'CV-{ahora:%Y%m%d}-{secrets.token_hex(3).upper()}',
        'fecha': f'{ahora:%d/%m/%Y %H:%M}',
        'usuario_id': request.user.pk,
        'usuario': request.user.get_full_name() or request.user.get_username(),
        'items': [{
            'codigo': item['espectaculo'].codigo,
            'titulo': item['espectaculo'].titulo,
            'sala': item['espectaculo'].sala,
            'fecha_funcion': f"{timezone.localtime(item['espectaculo'].fecha_funcion):%d/%m/%Y %H:%M}",
            'cantidad': item['cantidad'],
            'precio_unitario': int(item['precio_unitario']),
            'subtotal': int(item['subtotal']),
        } for item in items],
        'unidades': resumen['unidades'],
        'subtotal': int(resumen['subtotal']),
        'recargo': int(resumen['recargo']),
        'iva': int(resumen['iva']),
        'total': int(resumen['total']),
    }
    carrito.vaciar()
    messages.success(request, '¡Solicitud de entradas generada con éxito!')
    return redirect('reservas:comprobante')


@login_required
def comprobante(request):
    """Muestra el último comprobante del usuario autenticado."""
    datos = request.session.get(SESSION_COMPROBANTE)
    if not datos or datos.get('usuario_id') != request.user.pk:
        messages.info(request, 'No hay un comprobante reciente para mostrar.')
        return redirect('reservas:ver')
    return render(request, 'reservas/comprobante.html', {'comprobante': datos})
