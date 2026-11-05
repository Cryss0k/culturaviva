"""Prueba de humo: todas las rutas con nombre del contrato existen y la portada responde."""
from django.test import TestCase
from django.urls import reverse

RUTAS_SIN_ARGS = [
    'portal:inicio', 'portal:lista', 'portal:gestion_lista', 'portal:crear',
    'cuentas:registro', 'cuentas:login', 'cuentas:logout', 'cuentas:perfil',
    'reservas:ver', 'reservas:vaciar', 'reservas:confirmar', 'reservas:comprobante',
]
RUTAS_SLUG = ['portal:detalle', 'portal:editar', 'portal:eliminar']
RUTAS_ID = ['reservas:agregar', 'reservas:modificar', 'reservas:eliminar']


class ContratoUrlsTest(TestCase):
    def test_nombres_de_url_existen(self):
        for nombre in RUTAS_SIN_ARGS:
            self.assertTrue(reverse(nombre), nombre)
        for nombre in RUTAS_SLUG:
            self.assertTrue(reverse(nombre, kwargs={'slug': 'demo'}), nombre)
        for nombre in RUTAS_ID:
            self.assertTrue(reverse(nombre, kwargs={'espectaculo_id': 1}), nombre)

    def test_portada_responde_200(self):
        respuesta = self.client.get(reverse('portal:inicio'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'CulturaViva')
