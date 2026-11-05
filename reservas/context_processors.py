"""Context processor global (Cristian: tarea C9). Ya registrado en settings.TEMPLATES."""
from .carrito import Carrito


def carrito_contador(request):
    """Inyecta carrito_total_items en todas las plantillas (navbar)."""
    return {'carrito_total_items': len(Carrito(request))}
