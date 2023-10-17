from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Cliente, Pedido, Ubicacion, TipoPago, TipoEnvio, Producto

class PedidoModelTests(APITestCase):

    def test_pedido_reduce_stock(self):

        cliente = Cliente.objects.create(nombre="Carlos Juarez", email="cliente1@gmail.com", password="cliente1", telefono="54825613", fecha_nacimiento="1998-06-29")
        ubicacion = Ubicacion.objects.create(nombre="Oficina", direccion="21 avenida 10-25 zona 10", descripcion=None, telefono="23335332", nombre_recibe=None, cliente=cliente)
        tipopago = TipoPago.objects.create(nombre="Efectivo", descripcion="Pago en efectivo contra entrega o en local físico")
        tipoenvio = TipoEnvio.objects.create(nombre="Envío gratis", descripcion="Envío gratuito en el perímetro de la capital. Tiempo de entrega estimado: 2 días hábiles.", monto=0.0, stripe_id="shr_1O0XlcDcRClZvkQgl7pYjJjb")

        producto1 = Producto.objects.create(nombre="Cromatic Fast Dry", descripcion="Uso en acero estructural y mantenimiento en general. Ideal para trabajos pesados de protección. Proporciona máxima protección al acero en tanques, tuberías, señalizaciones y otras superficies de metal.", imagen="", existencia="75", alerta_existencia="50", precio=200, stripe_id="price_1O0TTwDcRClZvkQgjR1YOXyG")

        url = reverse('Pedido-list')
        data = {'nit': '5987245', 'nombre': 'Pedro Potter', 'telefono': '12345678', 'userid': cliente.pk, 'ubicacion': ubicacion.pk, 'tipopago': tipopago.pk, 'tipoenvio': tipoenvio.pk, 'productos': '[{"id":'+ str(producto1.pk) +',"cantidad":2}]'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Pedido.objects.count(), 1)
        self.assertEqual(Pedido.objects.get().nit, '5987245')
        self.assertEqual(Producto.objects.get().existencia, 73)
        
        #self.assertIs(future_question.was_published_recently(), False)

    '''def test_movimiento_nuevo_producto(self):
        cliente = Cliente(nombre="Carlos Juarez", email="cliente1@gmail.com", password="cliente1", telefono="54825613", fecha_nacimiento="1998-06-29")
        ubicacion = Ubicacion(nombre="Oficina", direccion="21 avenida 10-25 zona 10", descripcion=None, telefono="23335332", nombre_recibe=None, userid=10)
        tipopago = TipoPago(nombre="Efectivo", descripcion="Pago en efectivo contra entrega o en local físico")
        tipoenvio = TipoEnvio(nombre="Envío gratis", descripcion="Envío gratuito en el perímetro de la capital. Tiempo de entrega estimado: 2 días hábiles.", monto=0.0, stripe_id="shr_1O0XlcDcRClZvkQgl7pYjJjb")
        subtotal = 120
        total = 120
        pedido = Pedido(nit="5987245", nombre="Carlos Juarez", telefono="12345678", cliente=cliente, ubicacion=ubicacion, tipopago=tipopago, tipoenvio=tipoenvio, subtotal=subtotal, total=total, estado=0)
        
        #self.assertIs(future_question.was_published_recently(), False)'''