import json
import stripe

from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages

from django.db import IntegrityError, DataError
from django.db.models import Q, Sum
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, FileResponse

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from .permissions import UidPermission
from .models import Cliente, Producto, Categoria, Marca, DetalleCarrito, Ubicacion, UserPayment, TipoEnvio, TipoPago, Pedido, DetallePedido
from .serializers import ClienteSerializer, ClienteAuthSerializer, MarcaSerializer, CategoriaSerializer, ProductoThumbnailSerializer, ProductoAloneSerializer, ProductoDestacadoSerializer, UbicacionSerializer, PedidoSerializer, DetallePedidoSerializer, TipoEnvioSerializer, TipoPagoSerializer

from borb.pdf import Document
from borb.pdf import Page
from borb.pdf import SingleColumnLayout
from borb.pdf import Image
from borb.pdf import FixedColumnWidthTable as Table
from borb.pdf import Paragraph
from borb.pdf import Alignment
from borb.pdf import PDF
from borb.pdf import HexColor, X11Color
from borb.pdf import TableCell
from datetime import datetime
import random
from decimal import Decimal, getcontext
import io

from django.contrib.auth.models import User

class SuperUserViewSet(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = []

    def create(self, request, pk=None):
        if 'nombre' in request.data and 'email' in request.data and 'password' in request.data:
            user = User.objects.create_user(username=request.data['nombre'], email=request.data['email'], password=request.data['password'], is_staff=True, is_superuser=True, is_active=True)

            content = {'message': 'Superusuario creado con éxito.'}
            return Response(content, status=status.HTTP_201_CREATED)
        else:
            content = {'message': 'Datos incompletos'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

class ClienteViewSet(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = []

    def retrieve(self, request, pk=None):
        aux_cliente = None
        try:
            aux_cliente = Cliente.objects.get(pk=pk, estado=0)
        except ObjectDoesNotExist:
            content = {'message': 'No existe cliente'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ClienteSerializer(aux_cliente, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request, pk=None):
        if 'nombre' in request.data and 'email' in request.data and 'password' in request.data and 'telefono' in request.data and 'fecha_nacimiento' in request.data:
            hashed_password = make_password(request.data['password'])
            try:
                new_cliente = Cliente.objects.create(nombre=request.data['nombre'], email=request.data['email'], password = hashed_password, telefono=request.data['telefono'], fecha_nacimiento=request.data['fecha_nacimiento'])
            except IntegrityError as integrity_error:
                content = {'message': str(integrity_error)}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
            except DataError as data_error:
                content = {'message': str(data_error)}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
            except ValidationError as validation_error:
                content = {'message': str(validation_error)}
                return Response(content, status=status.HTTP_404_NOT_FOUND)

            cliente_serializer = ClienteSerializer(new_cliente, many=False)
            return Response(cliente_serializer.data, status=status.HTTP_201_CREATED)
        else:
            content = {'message': 'Datos incompletos'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        if 'nombre' in request.data and 'telefono' in request.data and 'fecha_nacimiento' in request.data:
            aux_cliente = None
            try:
                aux_cliente = Cliente.objects.get(pk=pk)
            except ObjectDoesNotExist:
                content = {'message': 'No existe cliente'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)

            try:
                aux_cliente.nombre = request.data['nombre']
                aux_cliente.telefono = request.data['telefono']
                aux_cliente.fecha_nacimiento = request.data['fecha_nacimiento']
                aux_cliente.save()
            except IntegrityError as integrity_error:
                content = {'message': str(integrity_error)}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
            except DataError as data_error:
                content = {'message': str(data_error)}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
            except ValidationError as validation_error:
                content = {'message': str(validation_error)}
                return Response(content, status=status.HTTP_404_NOT_FOUND)

            cliente_serializer = ClienteSerializer(aux_cliente, many=False)
            return Response(cliente_serializer.data, status=status.HTTP_201_CREATED)
        else:
            content = {'message': 'Datos incompletos'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk=None):
        if 'old_password' in request.data and 'password' in request.data:
            aux_cliente = None
            try:
                aux_cliente = Cliente.objects.get(pk=pk)
            except ObjectDoesNotExist:
                content = {'message': 'No existe cliente'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
            
            if not check_password(request.data['old_password'], aux_cliente.password):
                content = {'message': 'Contraseña actual no es correcta'}
                return Response(content, status=status.HTTP_403_FORBIDDEN)

            try:
                hashed_password = make_password(request.data['password'])
                aux_cliente.password = hashed_password
                aux_cliente.save()
            except IntegrityError as integrity_error:
                content = {'message': str(integrity_error)}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
            except DataError as data_error:
                content = {'message': str(data_error)}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
            except ValidationError as validation_error:
                content = {'message': str(validation_error)}
                return Response(content, status=status.HTTP_404_NOT_FOUND)

            cliente_serializer = ClienteSerializer(aux_cliente, many=False)
            return Response(cliente_serializer.data, status=status.HTTP_201_CREATED)
        else:
            content = {'message': 'Datos incompletos'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class LoginViewSet(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = []

    def retrieve(self, request, pk=None):
        aux_cliente = None
        try:
            aux_cliente = Cliente.objects.get(pk=pk, estado=0)
        except ObjectDoesNotExist:
            content = {'message': 'No existe cliente'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ClienteAuthSerializer(aux_cliente, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        if 'email' in request.data and 'password' in request.data:
            
            aux_cliente = None
            try:
                aux_cliente = Cliente.objects.get(email=request.data['email'], estado=0)
            except ObjectDoesNotExist:
                content = {'message': 'Usuario/contraseña incorrectos'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
            
            if check_password(request.data['password'], aux_cliente.password):
                cliente_serializer = ClienteAuthSerializer(aux_cliente, many=False)
                return Response(cliente_serializer.data, status=status.HTTP_200_OK)
            else:
                content = {'message': 'Usuario/contraseña incorrectos'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
            
        else:
            content = {'message': 'Datos incompletos'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

class HomeViewSet(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = []

    def list(self, request):
        
        productos_destacados = Producto.objects.filter(imagen_destacada__isnull=False, destacado=True, estado=0)
        productos_mas_vendidos = Producto.objects.filter(mas_vendido=True, estado=0)
        categorias = Categoria.objects.all().order_by('nombre')
        marcas = Marca.objects.all().order_by('nombre')
        
        content = {'productos_destacados': ProductoDestacadoSerializer(productos_destacados, many=True, context={"request": request}).data, 'productos_mas_vendidos' : ProductoThumbnailSerializer(productos_mas_vendidos, many=True, context={"request": request}).data, 'categorias' : CategoriaSerializer(categorias, many=True, context={"request": request}).data, 'marcas' : MarcaSerializer(marcas, many=True, context={"request": request}).data}
        return Response(content, status=status.HTTP_200_OK)
    
class CategoriaViewSet(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = []

    def list(self, request):
        categorias = Categoria.objects.all().order_by('nombre')
        content = CategoriaSerializer(categorias, many=True, context={"request": request})
        return Response(content.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        aux_categoria = None
        try:
            aux_categoria = Categoria.objects.get(pk=pk)
        except ObjectDoesNotExist:
            content = {'message': 'No existe categoria'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategoriaSerializer(aux_categoria, many=False, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class MarcaViewSet(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = []

    def list(self, request):
        marcas = Marca.objects.all().order_by('nombre')
        content = MarcaSerializer(marcas, many=True, context={"request": request})
        return Response(content.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        aux_marca = None
        try:
            aux_marca = Marca.objects.get(pk=pk)
        except ObjectDoesNotExist:
            content = {'message': 'No existe marca'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MarcaSerializer(aux_marca, many=False, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ProductoViewSet(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = []

    def retrieve(self, request, pk=None):
        aux_producto = None
        try:
            aux_producto = Producto.objects.get(pk=pk)
        except ObjectDoesNotExist:
            content = {'message': 'No existe producto'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductoAloneSerializer(aux_producto, many=False, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
class ProductoSearchViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    serializer_class = ProductoThumbnailSerializer
    
    def get_queryset(self):

        #Condiciones que incluyen todas las condiciones (and)
        search = self.request.query_params.get('search', None)
        filter1 = Q()
        if search is not None:
            filter1 = Q(nombre__lwsearch=search.lower())

        precio = self.request.query_params.get('precio', None)
        filter2 = Q()
        if precio is not None:
            filter2 = Q(descuento__isnull=False, descuento__lte=precio) | Q(descuento__isnull=True, precio__lte=precio)

        marcas = self.request.query_params.get('marcas', None)
        filter3 = Q()
        if marcas is not None:
            arr_marcas = json.loads(marcas)
            if len(arr_marcas) > 0:
                for marca in arr_marcas:
                    print(marca)
                    filter3 |= Q(marca__nombre__exact=marca)

        categorias = self.request.query_params.get('categorias', None)
        filter4 = Q()
        if categorias is not None:
            arr_categorias = json.loads(categorias)
            if len(categorias) > 0:
                for categoria in arr_categorias:
                    filter4 |= Q(categorias__nombre__exact=categoria)

        orden = self.request.query_params.get('orden', None)
        filter5 = 'nombre'
        if orden is not None:
            #az za hlow lowh
            if orden == 'za':
                filter5 = '-nombre'
            if orden == 'hlow':
                filter5 = '-precio'
            if orden == 'lowh':
                filter5 = 'precio'

        queryset = Producto.objects.filter(filter1, filter2, filter3, filter4).distinct().order_by(filter5)
        return queryset
    
class CarritoViewSet(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = [UidPermission]

    def create(self, request):
        
        if 'producto' in request.data and 'cantidad' in request.data:
            
            try:
                aux_producto = Producto.objects.get(pk=request.data['producto'])
            except ObjectDoesNotExist:
                content = {'message': 'No existe producto'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
            
            aux_cliente = Cliente.objects.get(pk=request.data['userid'])

            if int(request.data['cantidad']) > aux_producto.existencia:
                content = {'message': 'No se cuentan con existencias para el producto: ' + aux_producto.nombre}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                detalle_carrito = DetalleCarrito.objects.get(producto=aux_producto, cliente=aux_cliente)
                detalle_carrito.cantidad = request.data['cantidad']
                detalle_carrito.save()
            except ObjectDoesNotExist:
                detalle_carrito = DetalleCarrito.objects.create(producto=aux_producto, cliente=aux_cliente, cantidad=request.data['cantidad'])

            serializer = ClienteAuthSerializer(aux_cliente, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            content = {'message': 'Datos incompletos'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        
        aux_cliente = Cliente.objects.get(pk=request.data['userid'])
        if 'empty' in request.data:
            detalle_carrito = DetalleCarrito.objects.filter(cliente=aux_cliente)
            for detalle in detalle_carrito:
                detalle.delete()
        else:
            try:
                detalle_carrito = DetalleCarrito.objects.get(pk=pk)
                detalle_carrito.delete()
            except ObjectDoesNotExist:
                pass

        serializer = ClienteAuthSerializer(aux_cliente, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UbicacionViewSet(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = [UidPermission]

    def list(self, request):
        cliente = request.query_params.get('userid', None)
        if cliente is not None:
            try:
                aux_cliente = Cliente.objects.get(pk=cliente)
                ubicaciones = Ubicacion.objects.filter(cliente=aux_cliente, estado=0)
                serializer = UbicacionSerializer(ubicaciones, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                content = {'message': 'No existe cliente'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
        else:
            content = {'message': 'Datos incompletos'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            ubicacion = Ubicacion.objects.get(pk=pk, estado=0)
            serializer = UbicacionSerializer(ubicacion, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            content = {'message': 'No existe ubicacion'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request, pk=None):
        if 'nombre' in request.data and 'direccion' in request.data and 'telefono' in request.data and 'descripcion' in request.data and 'nombre_recibe' in request.data:
            
            aux_cliente = Cliente.objects.get(pk=request.data['userid'])
            try:
                new_ubicacion = Ubicacion.objects.create(nombre=request.data['nombre'], direccion=request.data['direccion'], telefono=request.data['telefono'], descripcion=request.data['descripcion'], nombre_recibe=request.data['nombre_recibe'], cliente=aux_cliente)
            except IntegrityError as integrity_error:
                content = {'message': str(integrity_error)}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
            except DataError as data_error:
                content = {'message': str(data_error)}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
            except ValidationError as validation_error:
                content = {'message': str(validation_error)}
                return Response(content, status=status.HTTP_404_NOT_FOUND)

            ubicacion = UbicacionSerializer(new_ubicacion, many=False)
            return Response(ubicacion.data, status=status.HTTP_201_CREATED)
        else:
            content = {'message': 'Datos incompletos'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        if 'nombre' in request.data and 'direccion' in request.data and 'telefono' in request.data and 'descripcion' in request.data and 'nombre_recibe' in request.data:
            
            aux_cliente = Cliente.objects.get(pk=request.data['userid'])
            try:
                ubicacion = Ubicacion.objects.get(pk=pk, cliente=aux_cliente, estado=0)
            except ObjectDoesNotExist:
                content = {'message': 'No existe ubicacion'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)

            try:
                ubicacion.nombre = request.data['nombre']
                ubicacion.direccion = request.data['direccion']
                ubicacion.telefono = request.data['telefono']
                ubicacion.descripcion = request.data['descripcion']
                ubicacion.nombre_recibe = request.data['nombre_recibe']
                ubicacion.save()
            except IntegrityError as integrity_error:
                content = {'message': str(integrity_error)}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
            except DataError as data_error:
                content = {'message': str(data_error)}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
            except ValidationError as validation_error:
                content = {'message': str(validation_error)}
                return Response(content, status=status.HTTP_404_NOT_FOUND)

            ubicacion_serializer = UbicacionSerializer(ubicacion, many=False)
            return Response(ubicacion_serializer.data, status=status.HTTP_201_CREATED)
        else:
            content = {'message': 'Datos incompletos'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        aux_cliente = Cliente.objects.get(pk=request.data['userid'])
        try:
            ubicacion = Ubicacion.objects.get(pk=pk, cliente=aux_cliente)
            ubicacion.estado = 1
            ubicacion.save()
            serializer = UbicacionSerializer(ubicacion, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            content = {'message': 'No existe ubicacion'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        
class TipoPagoViewSet(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = []

    def list(self, request):
        tipopagos = TipoPago.objects.all()
        content = TipoPagoSerializer(tipopagos, many=True, context={"request": request})
        return Response(content.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        aux_tipopago = None
        try:
            aux_tipopago = TipoPago.objects.get(pk=pk)
        except ObjectDoesNotExist:
            content = {'message': 'No existe tipo de pago'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TipoPagoSerializer(aux_tipopago, many=False, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class TipoEnvioViewSet(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = []

    def list(self, request):
        tipoenvios = TipoEnvio.objects.all()
        content = TipoEnvioSerializer(tipoenvios, many=True, context={"request": request})
        return Response(content.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        aux_tipoenvio = None
        try:
            aux_tipoenvio = TipoEnvio.objects.get(pk=pk)
        except ObjectDoesNotExist:
            content = {'message': 'No existe tipo de pago'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TipoEnvioSerializer(aux_tipoenvio, many=False, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
class PedidoViewSet(viewsets.ViewSet):
    permission_classes = [UidPermission]
    authentication_classes = []

    def list(self, request):
        cliente = request.query_params.get('userid', None)
        if cliente is not None:
            try:
                aux_cliente = Cliente.objects.get(pk=cliente)
                pedidos = Pedido.objects.filter(cliente=aux_cliente).order_by('-fecha', '-id')
                serializer = PedidoSerializer(pedidos, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                content = {'message': 'No existe cliente'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
        else:
            content = {'message': 'Datos incompletos'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        cliente = request.query_params.get('userid', None)
        if cliente is not None:
            try:
                aux_cliente = Cliente.objects.get(pk=cliente)
                pedido = Pedido.objects.get(pk=pk, cliente=aux_cliente)
                serializer = PedidoSerializer(pedido, many=False)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                content = {'message': 'No existe pedido'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
        else:
            content = {'message': 'Datos incompletos'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        if 'nit' in request.data and 'nombre' in request.data and 'telefono' in request.data and 'ubicacion' in request.data and 'tipopago' in request.data and 'productos' in request.data:
            cliente = Cliente.objects.get(pk=request.data['userid'])
            try:
                ubicacion = Ubicacion.objects.get(pk=request.data['ubicacion'])
            except ObjectDoesNotExist:
                content = {'message': 'No existe ubicacion'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
            
            try:
                tipopago = TipoPago.objects.get(pk=request.data['tipopago'])
            except ObjectDoesNotExist:
                content = {'message': 'No existe tipo de pago'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
            
            tipoenvio = None
            if 'tipoenvio' in request.data:
                try:
                    tipoenvio = TipoEnvio.objects.get(pk=request.data['tipoenvio'])
                except ObjectDoesNotExist:
                    content = {'message': 'No existe tipo de envío'}
                    return Response(content, status=status.HTTP_404_NOT_FOUND)
            
            subtotal = 0
            arr_productos = json.loads(request.data['productos'])
            for producto in arr_productos:
                pd = Producto.objects.get(pk=producto['id'])
                if producto['cantidad'] > pd.existencia:
                    content = {'message': 'No se cuentan con existencias para el producto: ' + pd.nombre}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
                subtotal += (pd.descuento if pd.descuento is not None else pd.precio) * producto['cantidad']
            total = subtotal
            if tipoenvio is not None:
                total += tipoenvio.monto

            new_pedido = Pedido.objects.create(nit=request.data['nit'], nombre=request.data['nombre'], telefono=request.data['telefono'], cliente=cliente, ubicacion=ubicacion, tipopago=tipopago, tipoenvio=tipoenvio, subtotal=subtotal, total=total, estado=0)

            for producto in arr_productos:
                pd = Producto.objects.get(pk=producto['id'])
                price = (pd.descuento if pd.descuento is not None else pd.precio)
                DetallePedido.objects.create(cantidad=producto['cantidad'], precio=price, pedido=new_pedido, producto=pd)

            pedido_serializer = PedidoSerializer(new_pedido, many=False)
            return Response(pedido_serializer.data, status=status.HTTP_201_CREATED)

        else:
            content = {'message': 'Datos incompletos'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

#Stripe VIEWS
class CardCheckoutViewSet(viewsets.ViewSet):
    permission_classes = [UidPermission]
    authentication_classes = []

    def create(self, request):
        if 'productos' in request.data and 'pedido' in request.data:
            arr_productos = json.loads(request.data['productos'])
            stripe.api_key = settings.STRIPE_SECRET_KEY
            checkout_session = stripe.checkout.Session.create(
                payment_method_types = ['card'],
                line_items = arr_productos,
                mode = 'payment',
                customer_creation = 'always',
                shipping_options = [
                    {'shipping_rate': 'shr_1O0XlcDcRClZvkQgl7pYjJjb'},
                    {'shipping_rate': 'shr_1O0XmbDcRClZvkQg1p0RECIJ'},
                    {'shipping_rate': 'shr_1O0Xo0DcRClZvkQgigRk0ywQ'},
                    {'shipping_rate': 'shr_1O0XowDcRClZvkQgirRWmB1Z'}
                ],
                success_url = settings.REDIRECT_DOMAIN + '/payment_successful?session_id={CHECKOUT_SESSION_ID}&pedido=' + request.data['pedido'],
                cancel_url = settings.REDIRECT_DOMAIN + '/payment_cancelled?pedido=' + request.data['pedido']
            )
            content = {'checkout_url': checkout_session.url}
            return Response(content, status=status.HTTP_200_OK)
        else:
            content = {'message': 'Datos incompletos'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    pedido = request.GET.get('pedido', None)
    tipoenvio = TipoEnvio.objects.get(stripe_id=session['shipping_cost']['shipping_rate'])
    aux_pedido = Pedido.objects.get(pk=pedido)
    aux_pedido.tipoenvio = tipoenvio
    aux_pedido.total = aux_pedido.subtotal + tipoenvio.monto
    aux_pedido.save()
    UserPayment.objects.create(pedido=aux_pedido, payment_bool=True, stripe_checkout_id=checkout_session_id)
    
    #Enviar a ruta success de FRONTEND
    return render(request, 'payment_successful.html')
        
def payment_cancelled(request):
    pedido = request.GET.get('pedido', None)
    aux_pedido = Pedido.objects.get(pk=pedido)
    aux_pedido.estado = 2
    aux_pedido.save()
    #Enviar a ruta success de FRONTEND
    return render(request, 'payment_cancelled.html')


def reciboDePedidoPk(request, pk):
    
    try:
        pedido = Pedido.objects.get(pk=pk)
    except ObjectDoesNotExist:
        messages.error(request, 'No existe pedido.')
        return HttpResponseRedirect('/admin/ferreteria/pedido/')
    
    # Create document
    pdf = Document()

    # Add page
    page = Page()
    pdf.add_page(page)

    page_layout = SingleColumnLayout(page)
    page_layout.vertical_margin = page.get_page_info().get_height() * Decimal(0.0025)
    page_layout.add(    
        Image(        
            "https://s3.stackabuse.com/media/articles/creating-an-invoice-in-python-with-ptext-1.png",
            width=Decimal(128),
            height=Decimal(128),
        )
    )

    table_001 = Table(number_of_rows=5, number_of_columns=3)
    
    table_001.add(Paragraph("[Street Address]"))
    table_001.add(Paragraph("Fecha", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
    datetime_object = pedido.fecha
    table_001.add(Paragraph("%d/%d/%d" % (datetime_object.day, datetime_object.month, datetime_object.year)))
    
    table_001.add(Paragraph("[City, State, ZIP Code]"))
    table_001.add(Paragraph("Pedido #", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT))
    table_001.add(Paragraph("%d" % pk))   
    
    table_001.add(Paragraph("[Phone]"))
    table_001.add(Paragraph(" "))
    table_001.add(Paragraph(" "))
    
    table_001.add(Paragraph("[Email Address]"))
    table_001.add(Paragraph(" "))
    table_001.add(Paragraph(" "))

    table_001.add(Paragraph("[Company Website]"))
    table_001.add(Paragraph(" "))
    table_001.add(Paragraph(" "))

    table_001.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))		
    table_001.no_borders()

    # Invoice information table  
    page_layout.add(table_001)
    
    # Empty paragraph for spacing  
    page_layout.add(Paragraph(" "))

    table_002 = Table(number_of_rows=6, number_of_columns=2)  
    table_002.add(  
        Paragraph(  
            "FACTURAR A",  
            background_color=HexColor("263238"),  
            font_color=X11Color("White"),  
        )  
    )  
    table_002.add(  
        Paragraph(  
            "ENVIAR A",  
            background_color=HexColor("263238"),  
            font_color=X11Color("White"),  
        )  
    )  
    table_002.add(Paragraph(pedido.nombre))    # BILLING  
    table_002.add(Paragraph(pedido.ubicacion.nombre_recibe if pedido.ubicacion.nombre_recibe is not None else pedido.nombre))    # SHIPPING
    table_002.add(Paragraph("NIT: " + pedido.nit))    # BILLING  
    table_002.add(Paragraph(pedido.ubicacion.direccion))    # SHIPPING  
    table_002.add(Paragraph(pedido.telefono)) # BILLING  
    table_002.add(Paragraph(pedido.ubicacion.telefono)) # SHIPPING  
    table_002.add(Paragraph(" "))             # BILLING  
    table_002.add(Paragraph(" "))             # SHIPPING  
    table_002.add(Paragraph(" "))             # BILLING  
    table_002.add(Paragraph(" "))             # SHIPPING  
    table_002.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))  
    table_002.no_borders()

    # Billing and shipping information table
    page_layout.add(table_002)

    table_003 = Table(number_of_rows=14, number_of_columns=4)  
    for h in ["NOMBRE", "CANTIDAD", "PRECIO UNITARIO", "TOTAL"]:  
        table_003.add(  
            TableCell(  
                Paragraph(h, font_color=X11Color("White")),  
                background_color=HexColor("000000"),  
            )  
        )  
  
    odd_color = HexColor("BBBBBB")  
    even_color = HexColor("FFFFFF")  
    for row_number, detalle in enumerate(pedido.detalle_pedido_pedido.all()):
        c = even_color if row_number % 2 == 0 else odd_color  
        table_003.add(TableCell(Paragraph(detalle.producto.nombre), background_color=c))
        table_003.add(TableCell(Paragraph(str(detalle.cantidad)), background_color=c))
        table_003.add(TableCell(Paragraph("Q " + "{:.2f}".format(detalle.precio)), background_color=c))
        table_003.add(TableCell(Paragraph("Q " + "{:.2f}".format(detalle.precio * detalle.cantidad)), background_color=c))
      
    # Optionally add some empty rows to have a fixed number of rows for styling purposes
    for row_number in range(len(pedido.detalle_pedido_pedido.all()), 10):  
        c = even_color if row_number % 2 == 0 else odd_color
        for _ in range(0, 4):  
            table_003.add(TableCell(Paragraph("-"), background_color=c))  
  
    table_003.add(TableCell(Paragraph("Subtotal", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT,), column_span=3,))  
    table_003.add(TableCell(Paragraph("Q " + "{:.2f}".format(pedido.subtotal), horizontal_alignment=Alignment.RIGHT)))  
    table_003.add(TableCell(Paragraph("Envío", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT,),column_span=3,))  
    table_003.add(TableCell(Paragraph("Q " + "{:.2f}".format(pedido.tipoenvio.monto), horizontal_alignment=Alignment.RIGHT)))  
    table_003.add(TableCell(Paragraph("Total", font="Helvetica-Bold", horizontal_alignment=Alignment.RIGHT  ), column_span=3,))  
    table_003.add(TableCell(Paragraph("Q " + "{:.2f}".format(pedido.total), horizontal_alignment=Alignment.RIGHT)))  
    table_003.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))  
    table_003.no_borders()

    # Itemized description
    page_layout.add(table_003)

    buffer = io.BytesIO()
    PDF.dumps(buffer, pdf)
    buffer.seek(0)

    response = HttpResponse(content=buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=recibo_' + str(pk) + '.pdf'
    return response