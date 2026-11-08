"""Pruebas de crear espectáculo: permisos, validaciones e imagen (Pablo: P7)."""
import shutil
import tempfile
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from PIL import Image

from catalogo.models import Espectaculo

from .base import BaseTestCase


class CrearEspectaculoTests(BaseTestCase):
    def test_anonimo_va_al_login(self):
        resp = self.client.get(reverse('portal:crear'))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith(reverse('cuentas:login')))

    def test_cliente_recibe_403(self):
        self.client.force_login(self.cliente)
        self.assertEqual(self.client.get(reverse('portal:crear')).status_code, 403)
        antes = Espectaculo.objects.count()
        self.client.post(reverse('portal:crear'), self.datos_formulario())
        self.assertEqual(Espectaculo.objects.count(), antes)

    def test_crear_ok_codigo_en_mayusculas_y_slug_automatico(self):
        self.client.force_login(self.staff)
        resp = self.client.post(reverse('portal:crear'), self.datos_formulario())
        self.assertRedirects(resp, reverse('portal:gestion_lista'), fetch_redirect_response=False)
        nuevo = Espectaculo.objects.get(codigo='TEA-500')
        self.assertEqual(nuevo.slug, 'obra-nueva')

    def test_slug_unico_si_el_titulo_se_repite(self):
        self.client.force_login(self.staff)
        self.client.post(reverse('portal:crear'), self.datos_formulario())
        self.client.post(reverse('portal:crear'), self.datos_formulario(codigo='TEA-501'))
        self.assertTrue(Espectaculo.objects.filter(slug='obra-nueva-2').exists())

    def test_crear_con_errores(self):
        self.client.force_login(self.staff)
        casos = {
            'codigo duplicado': ({'codigo': 'TEA-001'}, 'codigo'),
            'formato de codigo': ({'codigo': 'XX1'}, 'codigo'),
            'precio negativo': ({'precio_entrada': -5}, 'precio_entrada'),
            'sobre el aforo': ({'entradas_disponibles': 999}, 'entradas_disponibles'),
        }
        for nombre, (cambio, campo) in casos.items():
            with self.subTest(nombre):
                antes = Espectaculo.objects.count()
                resp = self.client.post(reverse('portal:crear'), self.datos_formulario(**cambio))
                self.assertEqual(resp.status_code, 200)
                self.assertIn(campo, resp.context['form'].errors)
                self.assertEqual(Espectaculo.objects.count(), antes)

    def test_crear_con_imagen(self):
        self.client.force_login(self.staff)
        carpeta = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, carpeta, True)
        buffer = BytesIO()
        Image.new('RGB', (10, 10), 'red').save(buffer, 'PNG')
        imagen = SimpleUploadedFile('poster.png', buffer.getvalue(), content_type='image/png')
        with override_settings(MEDIA_ROOT=carpeta):
            resp = self.client.post(reverse('portal:crear'), {**self.datos_formulario(), 'imagen': imagen})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Espectaculo.objects.get(codigo='TEA-500').imagen.name.startswith('espectaculos/'))
