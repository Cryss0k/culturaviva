"""Administración de Django (Cristian: tareas C5 y C6).

Esto es solo un registro mínimo para que el admin funcione desde el día 1.
Reemplazar por la configuración avanzada pedida en la rúbrica:
  - admin.site.site_header / site_title / index_title corporativos
  - @admin.register con list_display, list_filter, search_fields,
    list_editable y fieldsets
"""
from django.contrib import admin

from .models import Espectaculo, Genero


@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'activo')
    prepopulated_fields = {'slug': ('nombre',)}


@admin.register(Espectaculo)
class EspectaculoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'titulo', 'genero', 'precio_entrada', 'estado', 'activo')
    prepopulated_fields = {'slug': ('titulo',)}
