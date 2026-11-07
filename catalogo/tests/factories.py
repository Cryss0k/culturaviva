"""Funciones auxiliares para crear datos de prueba (compartidas con reservas)."""
from datetime import timedelta
from decimal import Decimal
from itertools import count

from django.utils import timezone
from django.utils.text import slugify

from catalogo.models import Espectaculo, Genero

_contador = count(1)


def crear_genero(nombre='Teatro', **extra):
    genero, _ = Genero.objects.get_or_create(
        nombre=nombre, defaults={'slug': slugify(nombre), **extra})
    return genero


def crear_espectaculo(genero=None, **extra):
    """Crea un espectáculo válido, disponible y con fecha futura. Se puede sobrescribir cualquier campo."""
    n = next(_contador)
    datos = {
        'genero': genero or crear_genero(),
        'codigo': f'TST-{n:03d}',
        'slug': f'espectaculo-{n}',
        'titulo': f'Espectáculo {n}',
        'descripcion': 'Descripción de prueba',
        'elenco': 'Elenco de prueba',
        'sala': 'Sala Principal',
        'fecha_funcion': timezone.now() + timedelta(days=10),
        'duracion_minutos': 90,
        'aforo': 100,
        'entradas_disponibles': 50,
        'precio_entrada': Decimal('10000'),
        'estado': Espectaculo.Estado.DISPONIBLE,
    }
    datos.update(extra)
    return Espectaculo.objects.create(**datos)
