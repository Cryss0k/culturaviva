from datetime import timedelta
from decimal import Decimal

from django.test import TestCase, override_settings
from django.utils import timezone

from catalogo.models import Espectaculo
from catalogo.tests.factories import crear_espectaculo
from reservas.carrito import Carrito, calcular_resumen


class SesionFalsa(dict):
    """Imita request.session: un diccionario con el atributo 'modified'."""
    modified = False


class PeticionFalsa:
    def __init__(self):
        self.session = SesionFalsa()


def nuevo_carrito():
    return Carrito(PeticionFalsa())


@override_settings(RECARGO_SERVICIO_PORCENTAJE=Decimal('0.10'),
                   IVA_PORCENTAJE=Decimal('0.19'), MAX_ENTRADAS_POR_COMPRA=6)
class CarritoTest(TestCase):
    def test_agregar_guarda_solo_id_y_cantidad(self):
        e = crear_espectaculo()
        carrito = nuevo_carrito()
        ok, _ = carrito.agregar(e.pk, 2)
        self.assertTrue(ok)
        self.assertEqual(carrito.session['carrito'], {str(e.pk): {'cantidad': 2}})
        self.assertTrue(carrito.session.modified)

    def test_agregar_acumula_cantidades(self):
        e = crear_espectaculo()
        carrito = nuevo_carrito()
        carrito.agregar(e.pk, 2)
        carrito.agregar(e.pk, 1)
        self.assertEqual(len(carrito), 3)

    def test_cantidades_invalidas(self):
        e = crear_espectaculo()
        for invalida in ('abc', 0, -1, None):
            ok, _ = nuevo_carrito().agregar(e.pk, invalida)
            self.assertFalse(ok, invalida)

    def test_no_supera_el_maximo_por_compra(self):
        e = crear_espectaculo(entradas_disponibles=50)
        carrito = nuevo_carrito()
        self.assertTrue(carrito.agregar(e.pk, 6)[0])
        ok, mensaje = carrito.agregar(e.pk, 1)
        self.assertFalse(ok)
        self.assertIn('Máximo 6', mensaje)
        self.assertEqual(len(carrito), 6)

    def test_no_supera_los_cupos(self):
        e = crear_espectaculo(entradas_disponibles=2)
        ok, mensaje = nuevo_carrito().agregar(e.pk, 3)
        self.assertFalse(ok)
        self.assertIn('Solo quedan 2', mensaje)

    def test_rechaza_agotado_suspendido_inactivo_y_pasado(self):
        casos = [
            crear_espectaculo(entradas_disponibles=0),
            crear_espectaculo(estado=Espectaculo.Estado.SUSPENDIDO),
            crear_espectaculo(activo=False),
            crear_espectaculo(fecha_funcion=timezone.now() - timedelta(days=1)),
        ]
        for e in casos:
            ok, _ = nuevo_carrito().agregar(e.pk, 1)
            self.assertFalse(ok, e.codigo)

    def test_espectaculo_inexistente(self):
        ok, _ = nuevo_carrito().agregar(99999, 1)
        self.assertFalse(ok)

    def test_modificar_cantidad(self):
        e = crear_espectaculo()
        carrito = nuevo_carrito()
        carrito.agregar(e.pk, 1)
        self.assertTrue(carrito.modificar(e.pk, 4)[0])
        self.assertEqual(len(carrito), 4)

    def test_modificar_a_cero_elimina_el_item(self):
        e = crear_espectaculo()
        carrito = nuevo_carrito()
        carrito.agregar(e.pk, 2)
        self.assertTrue(carrito.modificar(e.pk, 0)[0])
        self.assertEqual(len(carrito), 0)

    def test_modificar_item_que_no_esta_en_el_carrito(self):
        e = crear_espectaculo()
        self.assertFalse(nuevo_carrito().modificar(e.pk, 2)[0])

    def test_eliminar_y_vaciar(self):
        a, b = crear_espectaculo(), crear_espectaculo()
        carrito = nuevo_carrito()
        carrito.agregar(a.pk, 1)
        carrito.agregar(b.pk, 2)
        self.assertTrue(carrito.eliminar(a.pk)[0])
        self.assertEqual(len(carrito), 2)
        carrito.vaciar()
        self.assertEqual(len(carrito), 0)
        self.assertNotIn('carrito', carrito.session)

    def test_items_en_una_sola_consulta(self):
        a, b = crear_espectaculo(), crear_espectaculo()
        carrito = nuevo_carrito()
        carrito.agregar(a.pk, 1)
        carrito.agregar(b.pk, 2)
        with self.assertNumQueries(1):
            items = carrito.items()
        self.assertEqual(len(items), 2)
        self.assertEqual(items[1]['subtotal'], Decimal('20000'))

    def test_items_quita_espectaculos_dados_de_baja(self):
        e = crear_espectaculo()
        carrito = nuevo_carrito()
        carrito.agregar(e.pk, 1)
        Espectaculo.objects.filter(pk=e.pk).update(activo=False)
        self.assertEqual(carrito.items(), [])
        self.assertEqual(len(carrito), 0)

    def test_items_informa_error_si_se_agoto_despues(self):
        e = crear_espectaculo(entradas_disponibles=5)
        carrito = nuevo_carrito()
        carrito.agregar(e.pk, 3)
        Espectaculo.objects.filter(pk=e.pk).update(entradas_disponibles=1)
        items = carrito.items()
        self.assertIn('Solo quedan 1', items[0]['error'])
        self.assertTrue(carrito.validar(items))

    def test_validar_carrito_vacio(self):
        self.assertEqual(nuevo_carrito().validar(), ['Tu carrito está vacío.'])

    def test_resumen_con_recargo_e_iva(self):
        e = crear_espectaculo(precio_entrada=Decimal('10000'))
        carrito = nuevo_carrito()
        carrito.agregar(e.pk, 2)
        resumen = carrito.resumen()
        self.assertEqual(resumen['subtotal'], Decimal('20000'))
        self.assertEqual(resumen['recargo'], Decimal('2000'))
        self.assertEqual(resumen['iva'], Decimal('4180'))
        self.assertEqual(resumen['total'], Decimal('26180'))
        self.assertEqual(resumen['unidades'], 2)

    def test_redondeo_a_pesos_enteros(self):
        resumen = calcular_resumen(Decimal('9999'))
        self.assertEqual(resumen['recargo'], Decimal('1000'))
        self.assertEqual(resumen['iva'], Decimal('2090'))
        self.assertEqual(resumen['total'], Decimal('13089'))
