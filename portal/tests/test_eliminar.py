"""Pruebas de baja lógica (Pablo: P9)."""
from django.urls import reverse

from catalogo.models import Espectaculo

from .base import BaseTestCase


class EliminarEspectaculoTests(BaseTestCase):
    def test_cliente_recibe_403_y_no_se_da_de_baja(self):
        self.client.force_login(self.cliente)
        self.assertEqual(self.client.post(reverse('portal:eliminar', args=['obra-1'])).status_code, 403)
        self.assertTrue(Espectaculo.objects.get(slug='obra-1').activo)

    def test_pide_confirmacion_y_hace_baja_logica(self):
        self.client.force_login(self.staff)
        url = reverse('portal:eliminar', args=['obra-2'])
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertTrue(Espectaculo.objects.get(slug='obra-2').activo)  # GET no modifica nada
        resp = self.client.post(url)
        self.assertRedirects(resp, reverse('portal:gestion_lista'), fetch_redirect_response=False)
        espectaculo = Espectaculo.objects.get(slug='obra-2')  # el registro sigue existiendo
        self.assertFalse(espectaculo.activo)
        self.assertEqual(self.client.get(reverse('portal:detalle', args=['obra-2'])).status_code, 404)
