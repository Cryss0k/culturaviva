"""Pruebas de la validación de RUT (Pablo: P2)."""
from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from cuentas.validators import normalizar_rut, validar_rut


class ValidarRutTests(SimpleTestCase):
    def test_rut_valido_con_y_sin_formato(self):
        for rut in ('12.345.678-5', '12345678-5', '11.111.111-1', '7.654.321-6'):
            validar_rut(rut)  # no debe lanzar excepción

    def test_rut_con_digito_incorrecto(self):
        with self.assertRaises(ValidationError):
            validar_rut('12.345.678-9')

    def test_rut_con_formato_invalido(self):
        for rut in ('abc', '', '1-9', '12.345.678-X'):
            with self.assertRaises(ValidationError):
                validar_rut(rut)

    def test_normalizar(self):
        self.assertEqual(normalizar_rut('12.345.678-5'), '12345678-5')
