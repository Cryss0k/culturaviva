"""Pruebas de login, logout y perfil (Pablo: P3)."""
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from cuentas.models import Perfil


class LoginLogoutPerfilTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = User.objects.create_user('luis', 'luis@example.com', 'ClaveSegura#2026')
        Perfil.objects.create(usuario=cls.usuario, rut='11111111-1')

    def test_login_correcto_e_incorrecto(self):
        url = reverse('cuentas:login')
        malo = self.client.post(url, {'username': 'luis', 'password': 'mala'})
        self.assertEqual(malo.status_code, 200)
        bueno = self.client.post(url, {'username': 'luis', 'password': 'ClaveSegura#2026'})
        self.assertRedirects(bueno, reverse('portal:inicio'))

    def test_logout_solo_por_post(self):
        self.client.force_login(self.usuario)
        self.assertEqual(self.client.get(reverse('cuentas:logout')).status_code, 405)
        resp = self.client.post(reverse('cuentas:logout'))
        self.assertRedirects(resp, reverse('portal:inicio'))
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_perfil_exige_login(self):
        resp = self.client.get(reverse('cuentas:perfil'))
        self.assertRedirects(resp, f"{reverse('cuentas:login')}?next={reverse('cuentas:perfil')}")

    def test_perfil_edita_telefono(self):
        self.client.force_login(self.usuario)
        resp = self.client.post(reverse('cuentas:perfil'), {'telefono': '987654321'})
        self.assertRedirects(resp, reverse('cuentas:perfil'))
        self.usuario.perfil.refresh_from_db()
        self.assertEqual(self.usuario.perfil.telefono, '987654321')
