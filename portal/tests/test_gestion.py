"""Pruebas de la lista de gestión y sus permisos (Pablo: P10)."""
from django.urls import reverse

from .base import BaseTestCase


class GestionListaTests(BaseTestCase):
    def test_anonimo_va_al_login(self):
        resp = self.client.get(reverse('portal:gestion_lista'))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith(reverse('cuentas:login')))

    def test_cliente_recibe_403(self):
        self.client.force_login(self.cliente)
        self.assertEqual(self.client.get(reverse('portal:gestion_lista')).status_code, 403)

    def test_staff_ve_activos_e_inactivos(self):
        self.client.force_login(self.staff)
        resp = self.client.get(reverse('portal:gestion_lista'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'TEA-099')  # el inactivo también aparece en gestión
        self.assertContains(resp, 'TEA-001')
