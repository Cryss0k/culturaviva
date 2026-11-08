"""Prueba de integración del flujo del personal (Pablo: P11)."""
from django.urls import reverse

from catalogo.models import Espectaculo

from .base import BaseTestCase


class FlujoGestionTests(BaseTestCase):
    def test_crear_aparece_en_catalogo_y_la_baja_lo_oculta(self):
        self.client.force_login(self.staff)
        self.client.post(reverse('portal:crear'), self.datos_formulario(titulo='Estreno Especial'))
        espectaculo = Espectaculo.objects.get(codigo='TEA-500')

        publico = self.client.get(reverse('portal:lista'), {'q': 'Estreno'})
        self.assertEqual([e.pk for e in publico.context['pagina']], [espectaculo.pk])

        self.client.post(reverse('portal:eliminar', args=[espectaculo.slug]))
        publico = self.client.get(reverse('portal:lista'), {'q': 'Estreno'})
        self.assertEqual(publico.context['pagina'].paginator.count, 0)
        self.assertTrue(Espectaculo.objects.filter(pk=espectaculo.pk).exists())  # baja lógica
