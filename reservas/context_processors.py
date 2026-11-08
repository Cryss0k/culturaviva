"""Context processor global (Cristian: tarea C9). Registrado en settings.TEMPLATES."""
from .carrito import Carrito


def carrito_contador(request):
    """Inyecta carrito_total_items en todas las plantillas (contador del navbar).

    Solo lee la sesión (sin consultas a la BD). Si la petición no tiene sesión
    (p. ej. algunos tests o middleware desactivado) devuelve 0 en vez de fallar.
    """
    if not hasattr(request, 'session'):
        return {'carrito_total_items': 0}
    return {'carrito_total_items': len(Carrito(request))}
