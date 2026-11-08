"""Comando: python manage.py poblar_datos

Carga datos de demostración coherentes con una plataforma de venta de entradas:
  - 5 géneros y 10 espectáculos (con estados variados: disponible, agotado,
    suspendido y finalizado).
  - Usuarios de prueba: 'admin' (superusuario/staff) y 'cliente' (estándar),
    cada uno con su Perfil.
  - Imágenes de portada generadas con Pillow (omitir con --sin-imagenes).

Es idempotente: se puede ejecutar varias veces (update_or_create por código).
Las fechas son relativas a hoy, así que siempre quedan en el futuro (salvo el
espectáculo 'finalizado', que queda en el pasado a propósito).

Opciones:
  --limpiar        Borra espectáculos, géneros y usuarios de prueba antes de cargar.
  --sin-imagenes   No genera imágenes (útil en tests).
"""
import textwrap
from datetime import timedelta
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify

from catalogo.models import Espectaculo, Genero
from cuentas.models import Perfil

GENEROS = [
    {'nombre': 'Teatro', 'icono': 'bi-masks', 'color': (142, 68, 173),
     'descripcion': 'Obras clásicas y contemporáneas de artes escénicas.'},
    {'nombre': 'Música', 'icono': 'bi-music-note-beamed', 'color': (41, 128, 185),
     'descripcion': 'Conciertos, recitales y festivales en vivo.'},
    {'nombre': 'Danza', 'icono': 'bi-person-arms-up', 'color': (192, 57, 43),
     'descripcion': 'Ballet, danza contemporánea y bailes tradicionales.'},
    {'nombre': 'Stand-up', 'icono': 'bi-emoji-laughing', 'color': (211, 84, 0),
     'descripcion': 'Humor en vivo y espectáculos de comedia.'},
    {'nombre': 'Cine', 'icono': 'bi-film', 'color': (39, 174, 96),
     'descripcion': 'Ciclos, estrenos y muestras de cine.'},
]

# dias: desplazamiento respecto de hoy; hora: hora local de inicio.
ESPECTACULOS = [
    {'codigo': 'TEA-001', 'genero': 'Teatro', 'titulo': 'La casa de Bernarda Alba',
     'descripcion': 'Montaje contemporáneo del clásico de García Lorca sobre el encierro y el poder familiar.',
     'elenco': 'Compañía Teatro del Sur', 'sala': 'Sala Principal', 'dias': 21, 'hora': 20,
     'duracion': 110, 'aforo': 200, 'disponibles': 150, 'precio': 12000, 'estado': 'disponible'},
    {'codigo': 'TEA-002', 'genero': 'Teatro', 'titulo': 'Comedia en un acto',
     'descripcion': 'Una comedia ligera de enredos para toda la familia.',
     'elenco': 'Grupo Escena Viva', 'sala': 'Sala Experimental', 'dias': 28, 'hora': 19,
     'duracion': 75, 'aforo': 80, 'disponibles': 0, 'precio': 8000, 'estado': 'agotado'},
    {'codigo': 'MUS-001', 'genero': 'Música', 'titulo': 'Noche de jazz austral',
     'descripcion': 'Cuarteto de jazz con repertorio de autores del sur de Chile.',
     'elenco': 'Cuarteto Austral', 'sala': 'Sala Principal', 'dias': 35, 'hora': 21,
     'duracion': 120, 'aforo': 250, 'disponibles': 200, 'precio': 15000, 'estado': 'disponible'},
    {'codigo': 'MUS-002', 'genero': 'Música', 'titulo': 'Concierto sinfónico de primavera',
     'descripcion': 'La orquesta regional interpreta obras de Beethoven y Dvořák.',
     'elenco': 'Orquesta Regional', 'sala': 'Teatro Municipal', 'dias': 45, 'hora': 19,
     'duracion': 100, 'aforo': 400, 'disponibles': 320, 'precio': 20000, 'estado': 'disponible'},
    {'codigo': 'DAN-001', 'genero': 'Danza', 'titulo': 'Ballet contemporáneo: Raíces',
     'descripcion': 'Una mirada coreográfica a las raíces culturales de la región.',
     'elenco': 'Compañía Danza Viva', 'sala': 'Sala Principal', 'dias': 30, 'hora': 20,
     'duracion': 90, 'aforo': 220, 'disponibles': 180, 'precio': 14000, 'estado': 'disponible'},
    {'codigo': 'DAN-002', 'genero': 'Danza', 'titulo': 'Noche de tango',
     'descripcion': 'Show de tango con orquesta en vivo y milonga abierta al público.',
     'elenco': 'Dúo Buenos Aires', 'sala': 'Sala Experimental', 'dias': 14, 'hora': 21,
     'duracion': 80, 'aforo': 90, 'disponibles': 25, 'precio': 9000, 'estado': 'disponible'},
    {'codigo': 'STA-001', 'genero': 'Stand-up', 'titulo': 'Risas sin filtro',
     'descripcion': 'Cuatro comediantes, una hora y media de humor sin censura.',
     'elenco': 'Elenco Stand-up Chile', 'sala': 'Sala Experimental', 'dias': 18, 'hora': 21,
     'duracion': 90, 'aforo': 100, 'disponibles': 60, 'precio': 10000, 'estado': 'disponible'},
    {'codigo': 'STA-002', 'genero': 'Stand-up', 'titulo': 'Festival de humor al aire libre',
     'descripcion': 'Jornada de humor con artistas nacionales (suspendido por mal tiempo).',
     'elenco': 'Varios artistas', 'sala': 'Anfiteatro Municipal', 'dias': 60, 'hora': 18,
     'duracion': 180, 'aforo': 500, 'disponibles': 500, 'precio': 7000, 'estado': 'suspendido'},
    {'codigo': 'CIN-001', 'genero': 'Cine', 'titulo': 'Ciclo de cine chileno clásico',
     'descripcion': 'Proyección de clásicos del cine nacional con conversatorio.',
     'elenco': 'Cineclub Cultural', 'sala': 'Sala Audiovisual', 'dias': 10, 'hora': 19,
     'duracion': 120, 'aforo': 60, 'disponibles': 45, 'precio': 5000, 'estado': 'disponible'},
    {'codigo': 'CIN-002', 'genero': 'Cine', 'titulo': 'Maratón de cortometrajes',
     'descripcion': 'Selección de cortos de realizadores jóvenes (función ya realizada).',
     'elenco': 'Colectivo Audiovisual Sur', 'sala': 'Sala Audiovisual', 'dias': -15, 'hora': 18,
     'duracion': 150, 'aforo': 60, 'disponibles': 0, 'precio': 4000, 'estado': 'finalizado'},
]

USUARIOS = [
    {'username': 'admin', 'email': 'admin@culturaviva.cl', 'password': 'Admin12345!',
     'first_name': 'Administrador', 'es_staff': True, 'rut': '11111111-1',
     'telefono': '+56911111111', 'rol': Perfil.Rol.PRODUCTOR},
    {'username': 'cliente', 'email': 'cliente@culturaviva.cl', 'password': 'Cliente12345!',
     'first_name': 'Cliente de Prueba', 'es_staff': False, 'rut': '22222222-2',
     'telefono': '+56922222222', 'rol': Perfil.Rol.CLIENTE},
]


def _crear_imagen(titulo, color):
    """Genera una portada simple (800x450) con el título, usando Pillow."""
    from PIL import Image, ImageDraw, ImageFont

    imagen = Image.new('RGB', (800, 450), color)
    dibujo = ImageDraw.Draw(imagen)
    dibujo.rectangle([20, 20, 779, 429], outline=(255, 255, 255), width=4)
    try:
        fuente = ImageFont.load_default(size=40)
    except TypeError:  # versiones antiguas de Pillow
        fuente = ImageFont.load_default()
    y = 150
    for linea in textwrap.wrap(titulo, width=22):
        dibujo.text((50, y), linea, fill=(255, 255, 255), font=fuente)
        y += 55
    buffer = BytesIO()
    imagen.save(buffer, format='JPEG', quality=85)
    return ContentFile(buffer.getvalue())


class Command(BaseCommand):
    help = 'Carga datos de demostración (géneros, espectáculos y usuarios de prueba).'

    def add_arguments(self, parser):
        parser.add_argument('--limpiar', action='store_true',
                            help='Borra espectáculos, géneros y usuarios de prueba antes de cargar.')
        parser.add_argument('--sin-imagenes', action='store_true',
                            help='No genera imágenes de portada.')

    @transaction.atomic
    def handle(self, *args, **opciones):
        if opciones['limpiar']:
            self._limpiar()
        generos = self._crear_generos()
        espectaculos = self._crear_espectaculos(generos, not opciones['sin_imagenes'])
        self._crear_usuarios()

        self.stdout.write(self.style.SUCCESS(
            f'Listo: {len(generos)} géneros, {len(espectaculos)} espectáculos y '
            f'{len(USUARIOS)} usuarios de prueba.'))
        for u in USUARIOS:
            self.stdout.write(f"  usuario: {u['username']:<8} contraseña: {u['password']}")

    def _limpiar(self):
        # Orden importa: Espectaculo -> Genero (on_delete=PROTECT).
        Espectaculo.objects.all().delete()
        Genero.objects.all().delete()
        get_user_model().objects.filter(username__in=[u['username'] for u in USUARIOS]).delete()
        self.stdout.write(self.style.WARNING('Datos anteriores eliminados.'))

    def _crear_generos(self):
        generos = {}
        for datos in GENEROS:
            genero, _ = Genero.objects.update_or_create(
                nombre=datos['nombre'],
                defaults={'slug': slugify(datos['nombre']), 'descripcion': datos['descripcion'],
                          'icono': datos['icono'], 'activo': True},
            )
            generos[datos['nombre']] = genero
        return generos

    def _crear_espectaculos(self, generos, con_imagenes):
        colores = {g['nombre']: g['color'] for g in GENEROS}
        inicio_dia = timezone.localtime(timezone.now()).replace(minute=0, second=0, microsecond=0)
        creados = []
        for d in ESPECTACULOS:
            espectaculo, _ = Espectaculo.objects.update_or_create(
                codigo=d['codigo'],
                defaults={
                    'genero': generos[d['genero']],
                    'slug': slugify(d['titulo']),
                    'titulo': d['titulo'],
                    'descripcion': d['descripcion'],
                    'elenco': d['elenco'],
                    'sala': d['sala'],
                    'fecha_funcion': inicio_dia.replace(hour=d['hora']) + timedelta(days=d['dias']),
                    'duracion_minutos': d['duracion'],
                    'aforo': d['aforo'],
                    'entradas_disponibles': d['disponibles'],
                    'precio_entrada': d['precio'],
                    'estado': d['estado'],
                    'activo': True,
                },
            )
            if con_imagenes and not espectaculo.imagen:
                espectaculo.imagen.save(f"{d['codigo'].lower()}.jpg",
                                        _crear_imagen(d['titulo'], colores[d['genero']]), save=True)
            creados.append(espectaculo)
        return creados

    def _crear_usuarios(self):
        User = get_user_model()
        for datos in USUARIOS:
            usuario, _ = User.objects.get_or_create(username=datos['username'])
            usuario.email = datos['email']
            usuario.first_name = datos['first_name']
            usuario.is_staff = datos['es_staff']
            usuario.is_superuser = datos['es_staff']
            usuario.set_password(datos['password'])
            usuario.save()
            Perfil.objects.update_or_create(
                usuario=usuario,
                defaults={'rut': datos['rut'], 'telefono': datos['telefono'],
                          'rol_institucional': datos['rol']},
            )
