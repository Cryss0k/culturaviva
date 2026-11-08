from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .factories import crear_espectaculo


class AdminCorporativoTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.superusuario = get_user_model().objects.create_superuser('root', 'root@x.cl', 'clave12345')

    def setUp(self):
        self.client.force_login(self.superusuario)

    def test_titulos_corporativos(self):
        self.assertIn('CulturaViva', admin.site.site_header)
        self.assertIn('CulturaViva', admin.site.site_title)
        self.assertEqual(admin.site.index_title, 'Gestión Operativa de Recursos y Servicios')

    def test_listado_de_espectaculos(self):
        e = crear_espectaculo(titulo='Obra visible en admin')
        respuesta = self.client.get(reverse('admin:catalogo_espectaculo_changelist'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, e.codigo)

    def test_busqueda_por_codigo(self):
        e = crear_espectaculo()
        crear_espectaculo()
        respuesta = self.client.get(reverse('admin:catalogo_espectaculo_changelist'), {'q': e.codigo})
        self.assertContains(respuesta, e.codigo)
        self.assertEqual(respuesta.context['cl'].result_count, 1)

    def test_formulario_de_edicion_y_listado_de_generos(self):
        e = crear_espectaculo()
        url = reverse('admin:catalogo_espectaculo_change', args=[e.pk])
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertEqual(self.client.get(reverse('admin:catalogo_genero_changelist')).status_code, 200)

    def test_accion_desactivar(self):
        e = crear_espectaculo()
        respuesta = self.client.post(reverse('admin:catalogo_espectaculo_changelist'), {
            'action': 'desactivar', '_selected_action': [e.pk],
        })
        self.assertEqual(respuesta.status_code, 302)
        e.refresh_from_db()
        self.assertFalse(e.activo)
