"""Pruebas de los helpers de permisos (Pablo: P4)."""
from django.contrib.auth.models import AnonymousUser, User
from django.core.exceptions import PermissionDenied
from django.test import TestCase

from cuentas.permisos import es_staff, exige_staff


class PermisosTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cliente = User.objects.create_user('cliente', password='ClaveSegura#2026')
        cls.staff = User.objects.create_user('staff', password='ClaveSegura#2026', is_staff=True)

    def test_es_staff(self):
        self.assertFalse(es_staff(AnonymousUser()))
        self.assertFalse(es_staff(self.cliente))
        self.assertTrue(es_staff(self.staff))

    def test_exige_staff_lanza_403_a_quien_no_es_staff(self):
        self.assertTrue(exige_staff(self.staff))
        with self.assertRaises(PermissionDenied):
            exige_staff(self.cliente)
        with self.assertRaises(PermissionDenied):
            exige_staff(AnonymousUser())
