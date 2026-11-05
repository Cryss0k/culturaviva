"""Datos y utilidades compartidas por las pruebas del portal (Pablo)."""
from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from catalogo.models import Espectaculo, Genero


def crear_espectaculo(genero, n, **extra):
    datos = dict(
        genero=genero, codigo=f'TEA-{n:03d}', slug=f'obra-{n}', titulo=f'Obra {n}',
        descripcion='Descripción', elenco='Elenco', sala='Sala', duracion_minutos=90,
        fecha_funcion=timezone.now() + timedelta(days=n), aforo=100,
        entradas_disponibles=50, precio_entrada=1000 * n)
    datos.update(extra)
    return Espectaculo.objects.create(**datos)


class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.teatro = Genero.objects.create(nombre='Teatro', slug='teatro')
        cls.musica = Genero.objects.create(nombre='Música', slug='musica')
        for n in range(1, 11):  # 10 espectáculos de teatro -> 2 páginas de 9
            crear_espectaculo(cls.teatro, n)
        cls.concierto = crear_espectaculo(cls.musica, 11, titulo='Noche de jazz', codigo='MUS-001',
                                          slug='noche-de-jazz', descripcion='Concierto')
        cls.inactivo = crear_espectaculo(cls.teatro, 12, codigo='TEA-099', slug='oculto', activo=False)
        cls.cliente = User.objects.create_user('cliente', password='ClaveSegura#2026')
        cls.staff = User.objects.create_user('staff', password='ClaveSegura#2026', is_staff=True)

    def datos_formulario(self, **cambios):
        """Datos válidos para EspectaculoForm; se pueden sobrescribir campos."""
        datos = dict(
            genero=self.teatro.pk, codigo='tea-500', titulo='Obra Nueva', descripcion='Algo',
            elenco='Elenco', sala='Sala 1', fecha_funcion='2027-05-01T20:30',
            duracion_minutos=100, aforo=80, entradas_disponibles=80, precio_entrada=9000,
            estado='disponible', activo='on')
        datos.update(cambios)
        return datos
