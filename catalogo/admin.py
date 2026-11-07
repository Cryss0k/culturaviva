"""Administración de Django (Cristian: tareas C5 y C6)."""
from django.contrib import admin, messages
from django.db.models import Count
from django.utils.html import format_html

from .models import Espectaculo, Genero

# --- Identidad corporativa del panel -----------------------------------------
admin.site.site_header = 'CulturaViva Producciones - Panel de Control'
admin.site.site_title = 'CulturaViva Producciones Admin'
admin.site.index_title = 'Gestión Operativa de Recursos y Servicios'


@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'icono', 'total_espectaculos', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre', 'descripcion')
    list_editable = ('activo',)
    prepopulated_fields = {'slug': ('nombre',)}
    ordering = ('nombre',)

    def get_queryset(self, request):
        # Una sola consulta con COUNT en vez de una por fila (evita N+1).
        return super().get_queryset(request).annotate(_total=Count('espectaculos'))

    @admin.display(description='Espectáculos', ordering='_total')
    def total_espectaculos(self, obj):
        return obj._total


@admin.register(Espectaculo)
class EspectaculoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'titulo', 'genero', 'fecha_funcion', 'precio_entrada',
                    'entradas_disponibles', 'estado', 'activo')
    list_filter = ('genero', 'estado', 'activo')
    search_fields = ('codigo', 'titulo', 'elenco', 'sala', 'descripcion')
    # Edición rápida en la grilla (deben estar en list_display y no ser el primer campo).
    list_editable = ('precio_entrada', 'estado', 'activo')
    list_select_related = ('genero',)
    date_hierarchy = 'fecha_funcion'
    list_per_page = 15
    ordering = ('fecha_funcion',)
    prepopulated_fields = {'slug': ('titulo',)}
    readonly_fields = ('miniatura', 'creado', 'actualizado')
    actions = ('activar', 'desactivar')

    fieldsets = (
        ('Identificación', {'fields': ('codigo', 'slug', 'titulo', 'genero')}),
        ('Descripción', {'fields': ('descripcion', 'elenco')}),
        ('Función', {'fields': ('sala', 'fecha_funcion', 'duracion_minutos')}),
        ('Precios y cupos', {'fields': ('precio_entrada', 'aforo', 'entradas_disponibles')}),
        ('Multimedia', {'fields': ('imagen', 'miniatura')}),
        ('Estado y vigencia', {'fields': ('estado', 'activo')}),
        ('Auditoría', {'classes': ('collapse',), 'fields': ('creado', 'actualizado')}),
    )

    @admin.display(description='Vista previa')
    def miniatura(self, obj):
        if obj.pk and obj.imagen:
            return format_html('<img src="{}" style="height:60px;border-radius:4px;">', obj.imagen.url)
        return '-'

    @admin.action(description='Activar espectáculos seleccionados')
    def activar(self, request, queryset):
        total = queryset.update(activo=True)
        self.message_user(request, f'{total} espectáculo(s) activado(s).', messages.SUCCESS)

    @admin.action(description='Desactivar (baja lógica) espectáculos seleccionados')
    def desactivar(self, request, queryset):
        total = queryset.update(activo=False)
        self.message_user(request, f'{total} espectáculo(s) desactivado(s).', messages.SUCCESS)
