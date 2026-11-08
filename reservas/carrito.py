"""Carrito de entradas en request.session (Cristian: tarea C7).

Estructura en sesión (solo tipos JSON, nada de Decimal):
    request.session['carrito'] = {'12': {'cantidad': 2}, '7': {'cantidad': 1}}

Se guarda solo id y cantidad; el precio y el stock se leen de la BD en cada
cálculo, así el cliente nunca puede alterar los valores. Tras modificar el
diccionario se usa request.session.modified = True (ver _guardar).

Fórmula (redondeo a pesos enteros, ROUND_HALF_UP):
    subtotal = suma(precio_entrada * cantidad)
    recargo  = subtotal * settings.RECARGO_SERVICIO_PORCENTAJE
    iva      = (subtotal + recargo) * settings.IVA_PORCENTAJE
    total    = subtotal + recargo + iva

Todas las operaciones que modifican devuelven (ok, mensaje) para que la vista
muestre el resultado con el framework de mensajes.
"""
from decimal import ROUND_HALF_UP, Decimal

from django.conf import settings
from django.utils import timezone

from catalogo.models import Espectaculo

SESSION_CARRITO = 'carrito'
SESSION_COMPROBANTE = 'ultimo_comprobante'
_PESO = Decimal('1')


def _redondear(valor):
    """Redondea a pesos enteros (CLP no usa decimales)."""
    return valor.quantize(_PESO, rounding=ROUND_HALF_UP)


def calcular_resumen(subtotal):
    """Desglose económico a partir del subtotal. Devuelve dict de Decimal."""
    subtotal = _redondear(Decimal(subtotal))
    recargo = _redondear(subtotal * settings.RECARGO_SERVICIO_PORCENTAJE)
    iva = _redondear((subtotal + recargo) * settings.IVA_PORCENTAJE)
    return {'subtotal': subtotal, 'recargo': recargo, 'iva': iva, 'total': subtotal + recargo + iva}


class Carrito:
    """Colección transitoria de entradas guardada en la sesión HTTP."""

    def __init__(self, request):
        self.session = request.session
        # .get() (no setdefault) para no crear una sesión por cada visitante anónimo.
        self.datos = self.session.get(SESSION_CARRITO, {})

    # ---------------------------------------------------------------- utilidades
    def _guardar(self):
        self.session[SESSION_CARRITO] = self.datos
        self.session.modified = True

    @staticmethod
    def _a_entero(valor):
        try:
            return int(valor)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _obtener(espectaculo_id):
        return Espectaculo.objects.vigentes().filter(pk=espectaculo_id).first()

    @staticmethod
    def _validar(espectaculo, cantidad):
        """Devuelve un mensaje de error o None si la cantidad es válida para el espectáculo."""
        if espectaculo is None:
            return 'El espectáculo no existe o ya no está disponible.'
        if espectaculo.estado != Espectaculo.Estado.DISPONIBLE:
            return (f'«{espectaculo.titulo}» no está disponible para la venta '
                    f'(estado: {espectaculo.get_estado_display().lower()}).')
        if espectaculo.fecha_funcion <= timezone.now():
            return f'La función «{espectaculo.titulo}» ya se realizó.'
        if cantidad > settings.MAX_ENTRADAS_POR_COMPRA:
            return (f'Máximo {settings.MAX_ENTRADAS_POR_COMPRA} entradas por función '
                    f'en cada compra.')
        if espectaculo.entradas_disponibles <= 0:
            return f'Ya no quedan entradas para «{espectaculo.titulo}».'
        if cantidad > espectaculo.entradas_disponibles:
            return (f'Solo quedan {espectaculo.entradas_disponibles} entrada(s) '
                    f'para «{espectaculo.titulo}».')
        return None

    # --------------------------------------------------------------- operaciones
    def agregar(self, espectaculo_id, cantidad=1):
        """Valida y suma la cantidad a lo que ya hay en el carrito. Devuelve (ok, mensaje)."""
        cantidad = self._a_entero(cantidad)
        if cantidad is None or cantidad < 1:
            return False, 'Indica una cantidad válida (mínimo 1 entrada).'
        espectaculo = self._obtener(espectaculo_id)
        clave = str(espectaculo_id)
        nueva_cantidad = self.datos.get(clave, {}).get('cantidad', 0) + cantidad
        error = self._validar(espectaculo, nueva_cantidad)
        if error:
            return False, error
        self.datos[clave] = {'cantidad': nueva_cantidad}
        self._guardar()
        return True, f'Agregaste {cantidad} entrada(s) de «{espectaculo.titulo}» al carrito.'

    def modificar(self, espectaculo_id, cantidad):
        """Fija una nueva cantidad; si es 0 elimina el ítem. Devuelve (ok, mensaje)."""
        clave = str(espectaculo_id)
        if clave not in self.datos:
            return False, 'Ese espectáculo no está en tu carrito.'
        cantidad = self._a_entero(cantidad)
        if cantidad is None or cantidad < 0:
            return False, 'Indica una cantidad válida.'
        if cantidad == 0:
            return self.eliminar(espectaculo_id)
        error = self._validar(self._obtener(espectaculo_id), cantidad)
        if error:
            return False, error
        self.datos[clave] = {'cantidad': cantidad}
        self._guardar()
        return True, 'Cantidad actualizada.'

    def eliminar(self, espectaculo_id):
        """Quita un ítem del carrito. Devuelve (ok, mensaje)."""
        if self.datos.pop(str(espectaculo_id), None) is None:
            return False, 'Ese espectáculo no está en tu carrito.'
        self._guardar()
        return True, 'Quitaste el espectáculo del carrito.'

    def vaciar(self):
        """Elimina todo el carrito de la sesión."""
        self.session.pop(SESSION_CARRITO, None)
        self.datos = {}
        self.session.modified = True

    # ------------------------------------------------------------------- lectura
    def items(self):
        """Lista de dicts con espectaculo, cantidad, precio_unitario, subtotal y error.

        Hace una sola consulta (in_bulk + select_related). Los espectáculos que ya
        no existen o fueron dados de baja se eliminan del carrito automáticamente.
        'error' trae el motivo si la cantidad dejó de ser válida (p. ej. se agotó).
        """
        ids = [int(clave) for clave in self.datos]
        espectaculos = Espectaculo.objects.vigentes().select_related('genero').in_bulk(ids)
        resultado, huerfanos = [], []
        for clave, dato in self.datos.items():
            espectaculo = espectaculos.get(int(clave))
            if espectaculo is None:
                huerfanos.append(clave)
                continue
            cantidad = dato.get('cantidad', 0)
            resultado.append({
                'espectaculo': espectaculo,
                'cantidad': cantidad,
                'precio_unitario': espectaculo.precio_entrada,
                'subtotal': espectaculo.precio_entrada * cantidad,
                'error': self._validar(espectaculo, cantidad),
            })
        if huerfanos:
            for clave in huerfanos:
                self.datos.pop(clave, None)
            self._guardar()
        return resultado

    def resumen(self, items=None):
        """Desglose: subtotal, recargo, iva, total (Decimal) y unidades (int)."""
        items = self.items() if items is None else items
        subtotal = sum((item['subtotal'] for item in items), Decimal('0'))
        resumen = calcular_resumen(subtotal)
        resumen['unidades'] = sum(item['cantidad'] for item in items)
        return resumen

    def validar(self, items=None):
        """Lista de errores que impiden confirmar (vacía si todo está en orden)."""
        items = self.items() if items is None else items
        if not items:
            return ['Tu carrito está vacío.']
        return [item['error'] for item in items if item['error']]

    def __len__(self):
        """Total de unidades (alimenta el contador del navbar sin tocar la BD)."""
        return sum(dato.get('cantidad', 0) for dato in self.datos.values())
