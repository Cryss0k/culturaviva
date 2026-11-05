"""Carrito de entradas en request.session (Cristian: tarea C7).

Estructura en sesión (solo tipos JSON, nada de Decimal):
    request.session['carrito'] = {'12': {'cantidad': 2}, '7': {'cantidad': 1}}

Se guarda solo id y cantidad; precio y stock se leen de la BD en cada cálculo.
Tras modificar el diccionario usar: request.session.modified = True

Fórmula (redondeo a pesos enteros, ROUND_HALF_UP):
    subtotal = suma(precio_entrada * cantidad)
    recargo  = subtotal * settings.RECARGO_SERVICIO_PORCENTAJE
    iva      = (subtotal + recargo) * settings.IVA_PORCENTAJE
    total    = subtotal + recargo + iva
"""
SESSION_CARRITO = 'carrito'


class Carrito:
    """Interfaz acordada con el equipo. Implementar cada método."""

    def __init__(self, request):
        self.session = request.session
        self.datos = self.session.get(SESSION_CARRITO, {})

    def agregar(self, espectaculo_id, cantidad=1):
        """Valida (vigente, disponible, fecha futura, límite y stock) y suma. Devuelve (ok, mensaje)."""
        raise NotImplementedError

    def modificar(self, espectaculo_id, cantidad):
        """Cambia las unidades; si la cantidad es 0 elimina el ítem. Devuelve (ok, mensaje)."""
        raise NotImplementedError

    def eliminar(self, espectaculo_id):
        raise NotImplementedError

    def vaciar(self):
        raise NotImplementedError

    def items(self):
        """Lista de dicts: espectaculo, cantidad, subtotal de línea."""
        raise NotImplementedError

    def resumen(self):
        """Dict de Decimal: subtotal, recargo, iva, total."""
        raise NotImplementedError

    def __len__(self):
        """Total de unidades en el carrito (alimenta el contador del navbar)."""
        return sum(item.get('cantidad', 0) for item in self.datos.values())
