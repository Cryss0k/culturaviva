from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase, override_settings
from django.urls import reverse

from catalogo.tests.factories import crear_espectaculo


@override_settings(RECARGO_SERVICIO_PORCENTAJE=Decimal('0.10'),
                   IVA_PORCENTAJE=Decimal('0.19'), MAX_ENTRADAS_POR_COMPRA=6)
class ReservasVistasTest(TestCase):
    def setUp(self):
        self.espectaculo = crear_espectaculo(titulo='Obra de prueba', precio_entrada=Decimal('10000'))
        self.url_agregar = reverse('reservas:agregar', args=[self.espectaculo.pk])

    def _agregar(self, cantidad=2, **extra):
        return self.client.post(self.url_agregar, {'cantidad': cantidad, **extra})

    def _login(self):
        usuario = get_user_model().objects.create_user('comprador', 'c@x.cl', 'clave12345')
        self.client.force_login(usuario)
        return usuario

    def test_agregar_requiere_post(self):
        self.assertEqual(self.client.get(self.url_agregar).status_code, 405)

    def test_agregar_guarda_en_sesion_y_redirige_al_carrito(self):
        respuesta = self._agregar(2)
        self.assertRedirects(respuesta, reverse('reservas:ver'))
        self.assertEqual(self.client.session['carrito'], {str(self.espectaculo.pk): {'cantidad': 2}})

    def test_agregar_invalido_muestra_mensaje_de_error(self):
        respuesta = self._agregar(99)
        mensajes = [str(m) for m in get_messages(respuesta.wsgi_request)]
        self.assertTrue(any('Máximo' in m for m in mensajes))
        self.assertNotIn('carrito', self.client.session)

    def test_next_externo_no_se_respeta(self):
        respuesta = self._agregar(1, next='https://sitio-malicioso.example/')
        self.assertEqual(respuesta['Location'], reverse('reservas:ver'))

    def test_next_interno_si_se_respeta(self):
        respuesta = self._agregar(1, next='/espectaculos/')
        self.assertEqual(respuesta['Location'], '/espectaculos/')

    def test_carrito_muestra_desglose(self):
        self._agregar(2)
        respuesta = self.client.get(reverse('reservas:ver'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Obra de prueba')
        self.assertEqual(respuesta.context['resumen']['total'], Decimal('26180'))

    def test_carrito_vacio(self):
        respuesta = self.client.get(reverse('reservas:ver'))
        self.assertContains(respuesta, 'Tu carrito está vacío')

    def test_contador_global_del_navbar(self):
        self._agregar(3)
        respuesta = self.client.get(reverse('portal:inicio'))
        self.assertEqual(respuesta.context['carrito_total_items'], 3)

    def test_contador_en_cero_para_visitante_nuevo(self):
        respuesta = self.client.get(reverse('portal:inicio'))
        self.assertEqual(respuesta.context['carrito_total_items'], 0)

    def test_modificar_eliminar_y_vaciar(self):
        self._agregar(1)
        self.client.post(reverse('reservas:modificar', args=[self.espectaculo.pk]), {'cantidad': 4})
        self.assertEqual(self.client.session['carrito'][str(self.espectaculo.pk)]['cantidad'], 4)
        self.client.post(reverse('reservas:eliminar', args=[self.espectaculo.pk]))
        self.assertEqual(self.client.session['carrito'], {})
        self._agregar(2)
        self.client.post(reverse('reservas:vaciar'))
        self.assertNotIn('carrito', self.client.session)

    def test_confirmar_sin_login_redirige_al_login(self):
        self._agregar(1)
        respuesta = self.client.post(reverse('reservas:confirmar'))
        self.assertEqual(respuesta.status_code, 302)
        self.assertIn(reverse('cuentas:login'), respuesta['Location'])
        self.assertIn('carrito', self.client.session)  # no se pierde

    def test_confirmar_con_carrito_vacio_no_genera_comprobante(self):
        self._login()
        respuesta = self.client.post(reverse('reservas:confirmar'))
        self.assertRedirects(respuesta, reverse('reservas:ver'))
        self.assertNotIn('ultimo_comprobante', self.client.session)

    def test_confirmar_genera_comprobante_y_vacia_el_carrito(self):
        self._login()
        self._agregar(2)
        respuesta = self.client.post(reverse('reservas:confirmar'))
        self.assertRedirects(respuesta, reverse('reservas:comprobante'))
        self.assertNotIn('carrito', self.client.session)
        comprobante = self.client.session['ultimo_comprobante']
        self.assertTrue(comprobante['codigo'].startswith('CV-'))
        self.assertEqual(comprobante['total'], 26180)
        pagina = self.client.get(reverse('reservas:comprobante'))
        self.assertContains(pagina, comprobante['codigo'])
        self.assertContains(pagina, 'Obra de prueba')

    def test_confirmar_no_descuenta_stock(self):
        self._login()
        self._agregar(2)
        self.client.post(reverse('reservas:confirmar'))
        self.espectaculo.refresh_from_db()
        self.assertEqual(self.espectaculo.entradas_disponibles, 50)

    def test_comprobante_sin_datos_redirige_al_carrito(self):
        self._login()
        respuesta = self.client.get(reverse('reservas:comprobante'))
        self.assertRedirects(respuesta, reverse('reservas:ver'))

    def test_comprobante_de_otro_usuario_no_se_muestra(self):
        self._login()
        self._agregar(1)
        self.client.post(reverse('reservas:confirmar'))
        otro = get_user_model().objects.create_user('otro', 'o@x.cl', 'clave12345')
        sesion = self.client.session
        sesion['ultimo_comprobante']['usuario_id'] = otro.pk
        sesion.save()
        respuesta = self.client.get(reverse('reservas:comprobante'))
        self.assertRedirects(respuesta, reverse('reservas:ver'))
