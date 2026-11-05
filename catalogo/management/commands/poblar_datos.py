"""Comando: python manage.py poblar_datos  (Cristian: tarea C4)

PENDIENTE de implementar. Requisitos de la evaluación:
  - Al menos 4 géneros y 8 espectáculos coherentes con una productora cultural.
  - Usuarios de prueba: 'admin' (staff/superusuario) y 'cliente' (estándar).
  - Idempotente (update_or_create) y opción --limpiar.
Credenciales resultantes deben documentarse en el README.
"""
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Carga datos de demostración (géneros, espectáculos y usuarios de prueba).'

    def add_arguments(self, parser):
        parser.add_argument('--limpiar', action='store_true', help='Borra los datos antes de cargar.')

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('poblar_datos aún no está implementado (tarea C4).'))
