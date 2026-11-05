"""Formulario de gestión de espectáculos (Pablo: tareas P7 y P8)."""
from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from catalogo.models import Espectaculo
from cuentas.forms import BootstrapFormMixin


class EspectaculoForm(BootstrapFormMixin, forms.ModelForm):
    """Crear y editar espectáculos. El slug se genera solo a partir del título."""

    class Meta:
        model = Espectaculo
        exclude = ('slug', 'creado', 'actualizado')
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            'fecha_funcion': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def clean_codigo(self):
        """Código en mayúsculas y único (ignorando el propio registro al editar)."""
        codigo = self.cleaned_data['codigo'].strip().upper()
        repetido = Espectaculo.objects.filter(codigo=codigo).exclude(pk=self.instance.pk)
        if repetido.exists():
            raise ValidationError('Ya existe un espectáculo con ese código.')
        return codigo

    def clean_precio_entrada(self):
        precio = self.cleaned_data['precio_entrada']
        if precio < 0:
            raise ValidationError('El precio no puede ser negativo.')
        return precio

    def clean_entradas_disponibles(self):
        """No puede superar el aforo (aforo se limpia antes por el orden de los campos)."""
        disponibles = self.cleaned_data['entradas_disponibles']
        aforo = self.cleaned_data.get('aforo')
        if aforo is not None and disponibles > aforo:
            raise ValidationError('Las entradas disponibles no pueden superar el aforo.')
        return disponibles

    def save(self, commit=True):
        espectaculo = super().save(commit=False)
        if not espectaculo.slug:
            base = slugify(espectaculo.titulo) or 'espectaculo'
            slug, n = base, 2
            while Espectaculo.objects.filter(slug=slug).exclude(pk=espectaculo.pk).exists():
                slug, n = f'{base}-{n}', n + 1
            espectaculo.slug = slug
        if commit:
            espectaculo.save()
        return espectaculo
