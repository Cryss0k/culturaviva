from decimal import Decimal
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from django.test import TestCase
from django.utils import timezone

from catalogo.models import Espectaculo

from .factories import crear_espectaculo, crear_genero


class EspectaculoModeloTest(TestCase):
    def test_un_espectaculo_valido_pasa_full_clean(self):
        crear_espectaculo().full_clean()

    def test_str_incluye_codigo_y_titulo(self):
        e = crear_espectaculo(codigo='TEA-009', titulo='Hamlet')
        self.assertEqual(str(e), 'TEA-009 - Hamlet')

    def test_codigo_con_formato_invalido_falla(self):
        e = crear_espectaculo()
        e.codigo = 'abc'
        with self.assertRaises(ValidationError):
            e.full_clean()

    def test_precio_negativo_falla(self):
        e = crear_espectaculo()
        e.precio_entrada = Decimal('-1')
        with self.assertRaises(ValidationError):
            e.full_clean()

    def test_estado_fuera_de_choices_falla(self):
        e = crear_espectaculo()
        e.estado = 'inexistente'
        with self.assertRaises(ValidationError):
            e.full_clean()

    def test_entradas_no_pueden_superar_el_aforo(self):
        e = crear_espectaculo(aforo=100)
        e.entradas_disponibles = 101
        with self.assertRaises(ValidationError) as ctx:
            e.full_clean()
        self.assertIn('entradas_disponibles', ctx.exception.message_dict)

    def test_no_se_puede_borrar_un_genero_con_espectaculos(self):
        e = crear_espectaculo()
        with self.assertRaises(ProtectedError):
            e.genero.delete()

    def test_puede_reservar(self):
        self.assertTrue(crear_espectaculo().puede_reservar)
        self.assertFalse(crear_espectaculo(entradas_disponibles=0).puede_reservar)
        self.assertFalse(crear_espectaculo(estado=Espectaculo.Estado.SUSPENDIDO).puede_reservar)
        self.assertFalse(crear_espectaculo(activo=False).puede_reservar)

    def test_es_futuro(self):
        self.assertTrue(crear_espectaculo().es_futuro)
        pasado = crear_espectaculo(fecha_funcion=timezone.now() - timedelta(days=1))
        self.assertFalse(pasado.es_futuro)


class EspectaculoQuerySetTest(TestCase):
    def test_vigentes_excluye_dados_de_baja(self):
        activo = crear_espectaculo()
        crear_espectaculo(activo=False)
        self.assertEqual(list(Espectaculo.objects.vigentes()), [activo])

    def test_disponibles_aplica_todas_las_reglas(self):
        bueno = crear_espectaculo()
        crear_espectaculo(activo=False)
        crear_espectaculo(estado=Espectaculo.Estado.AGOTADO)
        crear_espectaculo(entradas_disponibles=0)
        crear_espectaculo(fecha_funcion=timezone.now() - timedelta(days=1))
        self.assertEqual(list(Espectaculo.objects.disponibles()), [bueno])

    def test_del_genero_filtra_por_slug(self):
        musica = crear_genero('Música')
        e = crear_espectaculo(genero=musica)
        crear_espectaculo()  # otro género
        self.assertEqual(list(Espectaculo.objects.del_genero('musica')), [e])

    def test_con_genero_evita_consultas_extra(self):
        crear_espectaculo()
        crear_espectaculo()
        with self.assertNumQueries(1):
            for e in Espectaculo.objects.con_genero():
                _ = e.genero.nombre
