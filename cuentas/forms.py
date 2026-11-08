"""Formularios de autenticación y perfil (Pablo: tareas P2 y P3)."""
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction

from .models import Perfil
from .validators import normalizar_rut, validar_rut


class BootstrapFormMixin:
    """Agrega las clases de Bootstrap 5 a todos los widgets del formulario."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            widget = campo.widget
            if isinstance(widget, forms.CheckboxInput):
                clase = 'form-check-input'
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                clase = 'form-select'
            else:
                clase = 'form-control'
            widget.attrs['class'] = f"{widget.attrs.get('class', '')} {clase}".strip()


class LoginForm(BootstrapFormMixin, AuthenticationForm):
    """Login con estilos de Bootstrap."""


class RegistroForm(BootstrapFormMixin, UserCreationForm):
    """Crea un User y su Perfil dentro de una misma transacción."""

    email = forms.EmailField(label='Correo electrónico')
    rut = forms.CharField(label='RUT', max_length=12, validators=[validar_rut],
                          help_text='Ejemplo: 12.345.678-5')
    telefono = forms.CharField(label='Teléfono', max_length=15, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Ya existe una cuenta con este correo.')
        return email

    def clean_rut(self):
        rut = normalizar_rut(self.cleaned_data['rut'])
        if Perfil.objects.filter(rut=rut).exists():
            raise forms.ValidationError('Este RUT ya está registrado.')
        return rut

    def save(self, commit=True):
        with transaction.atomic():
            user = super().save(commit=False)
            user.email = self.cleaned_data['email']
            user.save()
            Perfil.objects.create(
                usuario=user,
                rut=self.cleaned_data['rut'],
                telefono=self.cleaned_data['telefono'],
            )
        return user


class PerfilForm(BootstrapFormMixin, forms.ModelForm):
    """Permite editar solo el teléfono; el RUT y el rol no se modifican."""

    class Meta:
        model = Perfil
        fields = ('telefono',)
