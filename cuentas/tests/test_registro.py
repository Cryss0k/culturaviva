"""Pruebas del registro de usuarios (Pablo: P2)."""
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from cuentas.models import Perfil


class RegistroTests(TestCase):
    datos = {
        'username': 'ana', 'email': 'ana@example.com',
        'password1': 'ClaveSegura#2026', 'password2': 'ClaveSegura#2026',
        'rut': '12.345.678-5', 'telefono': '+56911112222',
    }

    def test_registro_crea_user_y_perfil_y_abre_sesion(self):
        resp = self.client.post(reverse('cuentas:registro'), self.datos)
        self.assertRedirects(resp, reverse('portal:inicio'))
        usuario = User.objects.get(username='ana')
        self.assertEqual(usuario.perfil.rut, '12345678-5')
        self.assertEqual(usuario.perfil.rol_institucional, Perfil.Rol.CLIENTE)
        self.assertEqual(int(self.client.session['_auth_user_id']), usuario.pk)

    def test_rut_invalido_no_crea_nada(self):
        resp = self.client.post(reverse('cuentas:registro'), {**self.datos, 'rut': '12.345.678-9'})
        self.assertEqual(resp.status_code, 200)
        self.assertIn('rut', resp.context['form'].errors)
        self.assertFalse(User.objects.exists())
        self.assertFalse(Perfil.objects.exists())

    def test_rut_duplicado(self):
        self.client.post(reverse('cuentas:registro'), self.datos)
        self.client.logout()
        otro = {**self.datos, 'username': 'beto', 'email': 'beto@example.com'}
        resp = self.client.post(reverse('cuentas:registro'), otro)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(User.objects.count(), 1)
