import tempfile
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, override_settings

from catalogo.models import Espectaculo, Genero


def ejecutar(*argumentos):
    call_command('poblar_datos', *argumentos, stdout=StringIO())


class PoblarDatosTest(TestCase):
    def test_carga_los_minimos_pedidos(self):
        ejecutar('--sin-imagenes')
        self.assertGreaterEqual(Genero.objects.count(), 4)
        self.assertGreaterEqual(Espectaculo.objects.count(), 8)

    def test_crea_usuarios_admin_y_estandar(self):
        ejecutar('--sin-imagenes')
        User = get_user_model()
        admin = User.objects.get(username='admin')
        cliente = User.objects.get(username='cliente')
        self.assertTrue(admin.is_staff and admin.is_superuser)
        self.assertFalse(cliente.is_staff)
        self.assertTrue(cliente.check_password('Cliente12345!'))

    def test_es_idempotente(self):
        ejecutar('--sin-imagenes')
        generos, espectaculos = Genero.objects.count(), Espectaculo.objects.count()
        usuarios = get_user_model().objects.count()
        ejecutar('--sin-imagenes')
        self.assertEqual(Genero.objects.count(), generos)
        self.assertEqual(Espectaculo.objects.count(), espectaculos)
        self.assertEqual(get_user_model().objects.count(), usuarios)

    def test_hay_estados_variados_y_los_datos_son_validos(self):
        ejecutar('--sin-imagenes')
        estados = set(Espectaculo.objects.values_list('estado', flat=True))
        self.assertEqual(estados, {'disponible', 'agotado', 'suspendido', 'finalizado'})
        for espectaculo in Espectaculo.objects.all():
            espectaculo.full_clean()

    def test_limpiar_reinicia_los_datos(self):
        crear = Genero.objects.create(nombre='Sobrante', slug='sobrante')
        ejecutar('--limpiar', '--sin-imagenes')
        self.assertFalse(Genero.objects.filter(pk=crear.pk).exists())
        self.assertGreaterEqual(Espectaculo.objects.count(), 8)

    def test_genera_imagenes_de_portada(self):
        with tempfile.TemporaryDirectory() as carpeta:
            with override_settings(MEDIA_ROOT=carpeta):
                ejecutar()
                self.assertTrue(all(e.imagen for e in Espectaculo.objects.all()))
