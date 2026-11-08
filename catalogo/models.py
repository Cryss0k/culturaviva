"""Modelos del catálogo. Contrato definido en docs/GUIA_EQUIPO.md (sección modelos).

Propiedad de Cristian. Cambios de campos: avisar por issue y migrar rápido.
"""
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

from .managers import EspectaculoQuerySet
from .validators import validar_codigo


class Genero(models.Model):
    """Entidad de contexto: clasificación artística (Teatro, Música, Danza...)."""

    nombre = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True)
    descripcion = models.TextField(blank=True)
    icono = models.CharField(max_length=40, blank=True, help_text='Clase de Bootstrap Icons (ej: bi-mic)')
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'género'
        verbose_name_plural = 'géneros'

    def __str__(self):
        return self.nombre


class Espectaculo(models.Model):
    """Entidad principal gestionable: una función con sala, aforo, valor y fecha."""

    class Estado(models.TextChoices):
        DISPONIBLE = 'disponible', 'Disponible'
        AGOTADO = 'agotado', 'Agotado'
        SUSPENDIDO = 'suspendido', 'Suspendido'
        FINALIZADO = 'finalizado', 'Finalizado'

    genero = models.ForeignKey(Genero, on_delete=models.PROTECT, related_name='espectaculos')
    codigo = models.CharField(max_length=20, unique=True, validators=[validar_codigo])
    slug = models.SlugField(max_length=160, unique=True)
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    elenco = models.CharField(max_length=150)
    sala = models.CharField(max_length=100)
    fecha_funcion = models.DateTimeField()
    duracion_minutos = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    aforo = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    entradas_disponibles = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    precio_entrada = models.DecimalField(
        max_digits=10, decimal_places=0, validators=[MinValueValidator(0)],
        help_text='Valor por entrada en pesos chilenos (CLP).',
    )
    estado = models.CharField(max_length=12, choices=Estado.choices, default=Estado.DISPONIBLE)
    imagen = models.ImageField(upload_to='espectaculos/', blank=True)
    activo = models.BooleanField(default=True, help_text='Baja lógica: desmarcar para ocultar sin borrar.')
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    objects = EspectaculoQuerySet.as_manager()

    class Meta:
        ordering = ['fecha_funcion']
        verbose_name = 'espectáculo'
        verbose_name_plural = 'espectáculos'

    def __str__(self):
        return f'{self.codigo} - {self.titulo}'

    def clean(self):
        """Regla de negocio: no se pueden ofrecer más entradas que el aforo de la sala."""
        super().clean()
        if (self.entradas_disponibles is not None and self.aforo is not None
                and self.entradas_disponibles > self.aforo):
            raise ValidationError({
                'entradas_disponibles': 'Las entradas disponibles no pueden superar el aforo.',
            })

    def get_absolute_url(self):
        return reverse('portal:detalle', kwargs={'slug': self.slug})

    @property
    def es_futuro(self):
        """True si la función aún no se realiza."""
        return self.fecha_funcion > timezone.now()

    @property
    def puede_reservar(self):
        """True si se puede vender: vigente, disponible y con cupos."""
        return self.activo and self.estado == self.Estado.DISPONIBLE and self.entradas_disponibles > 0
