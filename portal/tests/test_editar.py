"""Pruebas de editar espectáculo (Pablo: P8)."""
from django.urls import reverse

from catalogo.models import Espectaculo

from .base import BaseTestCase


class EditarEspectaculoTests(BaseTestCase):
    def test_cliente_recibe_403(self):
        self.client.force_login(self.cliente)
        self.assertEqual(self.client.get(reverse('portal:editar', args=['obra-1'])).status_code, 403)

    def test_editar_precargado_y_conserva_su_propio_codigo(self):
        self.client.force_login(self.staff)
        url = reverse('portal:editar', args=['obra-1'])
        resp = self.client.get(url)
        self.assertEqual(resp.context['form'].initial['codigo'], 'TEA-001')
        self.assertContains(resp, 'datetime-local')
        datos = self.datos_formulario(codigo='TEA-001', titulo='Obra 1 editada')
        resp = self.client.post(url, datos)
        self.assertRedirects(resp, reverse('portal:gestion_lista'), fetch_redirect_response=False)
        editado = Espectaculo.objects.get(codigo='TEA-001')
        self.assertEqual(editado.titulo, 'Obra 1 editada')
        self.assertEqual(editado.slug, 'obra-1')  # el slug no cambia

    def test_no_permite_usar_el_codigo_de_otro_espectaculo(self):
        self.client.force_login(self.staff)
        resp = self.client.post(reverse('portal:editar', args=['obra-1']),
                                self.datos_formulario(codigo='TEA-002'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('codigo', resp.context['form'].errors)
