"""Pruebas del catálogo público: lista, búsqueda, filtros, orden y paginación (Pablo: P5)."""
from django.urls import reverse

from .base import BaseTestCase


class CatalogoPublicoTests(BaseTestCase):
    def test_lista_publica_pagina_de_9(self):
        resp = self.client.get(reverse('portal:lista'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['pagina']), 9)
        self.assertNotContains(resp, 'oculto')  # el inactivo no aparece
        resp2 = self.client.get(reverse('portal:lista'), {'page': 2})
        self.assertEqual(len(resp2.context['pagina']), 2)

    def test_paginacion_conserva_filtros(self):
        resp = self.client.get(reverse('portal:lista'), {'genero': 'teatro', 'orden': 'titulo'})
        self.assertContains(resp, 'genero=teatro&amp;orden=titulo&amp;page=2')

    def test_busqueda_por_titulo_y_codigo(self):
        resp = self.client.get(reverse('portal:lista'), {'q': 'jazz'})
        self.assertEqual([e.slug for e in resp.context['pagina']], ['noche-de-jazz'])
        resp = self.client.get(reverse('portal:lista'), {'q': 'mus-001'})
        self.assertEqual(len(resp.context['pagina']), 1)

    def test_filtro_por_genero(self):
        resp = self.client.get(reverse('portal:lista'), {'genero': 'musica'})
        self.assertEqual(resp.context['pagina'].paginator.count, 1)

    def test_orden_valido_e_invalido(self):
        resp = self.client.get(reverse('portal:lista'), {'orden': '-precio_entrada'})
        precios = [e.precio_entrada for e in resp.context['pagina']]
        self.assertEqual(precios, sorted(precios, reverse=True))
        resp = self.client.get(reverse('portal:lista'), {'orden': 'password; DROP TABLE'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['orden_actual'], 'fecha_funcion')

    def test_inicio_responde(self):
        self.assertEqual(self.client.get(reverse('portal:inicio')).status_code, 200)
