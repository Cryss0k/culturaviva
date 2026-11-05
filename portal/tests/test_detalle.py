"""Pruebas del detalle por slug (Pablo: P6)."""
from django.urls import reverse

from .base import BaseTestCase, crear_espectaculo


class DetalleTests(BaseTestCase):
    def test_detalle_ok_y_404_si_inactivo_o_inexistente(self):
        self.assertEqual(self.client.get(reverse('portal:detalle', args=['obra-1'])).status_code, 200)
        self.assertEqual(self.client.get(reverse('portal:detalle', args=['oculto'])).status_code, 404)
        self.assertEqual(self.client.get(reverse('portal:detalle', args=['no-existe'])).status_code, 404)

    def test_detalle_disponible_muestra_formulario_de_compra(self):
        resp = self.client.get(reverse('portal:detalle', args=['obra-1']))
        self.assertContains(resp, 'name="cantidad"')

    def test_detalle_agotado_no_muestra_formulario_de_compra(self):
        agotado = crear_espectaculo(self.teatro, 20, estado='agotado', slug='agotada', codigo='TEA-020')
        resp = self.client.get(reverse('portal:detalle', args=[agotado.slug]))
        self.assertNotContains(resp, 'name="cantidad"')
