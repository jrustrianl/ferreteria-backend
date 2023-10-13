from rest_framework import serializers

from django.db.models import Sum, F
from .models import Cliente, Producto, Marca, Categoria, DetalleCarrito, MetaProducto, Ubicacion, Pedido, DetallePedido, TipoPago, TipoEnvio

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ['id', 'nombre', 'descripcion', 'icono', 'imagen_destacada']

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'icono', 'imagen_destacada']
        
class TipoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPago
        fields = ['id', 'nombre', 'descripcion']

class TipoEnvioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEnvio
        fields = ['id', 'nombre', 'descripcion', 'monto']
class MetaProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaProducto
        fields = ['key', 'value']

class ProductoThumbnailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'miniatura', 'precio', 'descuento']

class ProductoDestacadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'imagen_destacada', 'precio', 'descuento']

class ProductoAloneSerializer(serializers.ModelSerializer):
    marca = MarcaSerializer(required=True)
    categorias = CategoriaSerializer(many=True, read_only=True)
    meta_productos = MetaProductoSerializer(many=True, read_only=True)

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'imagen', 'precio', 'descuento', 'marca', 'categorias', 'meta_productos']

class CarritoSerializer(serializers.ModelSerializer):
    producto = ProductoThumbnailSerializer()
    class Meta:
        model = DetalleCarrito
        fields = ['id', 'producto', 'cantidad']

class ClienteAuthSerializer(serializers.ModelSerializer):
    carrito = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'email', 'subtotal', 'carrito']

    def get_subtotal(self, instance):
        return instance.carrito.aggregate(total=Sum(F('carritos_producto__producto__precio') * F('carritos_producto__cantidad')))['total']
    
    def get_carrito(self, instance):
        aux_items = DetalleCarrito.objects.filter(cliente=instance).order_by('producto__nombre')
        return CarritoSerializer(aux_items, many=True, context=self.context).data

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'telefono', 'fecha_nacimiento']
        
class UbicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ubicacion
        fields = ['id', 'nombre', 'direccion', 'descripcion', 'telefono', 'nombre_recibe']

class ProductoStripeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['nombre', 'stripe_id']

class DetallePedidoSerializer(serializers.ModelSerializer):
    producto = ProductoStripeSerializer()
    class Meta:
        model = DetallePedido
        fields = ['id', 'producto', 'cantidad', 'precio']

class PedidoSerializer(serializers.ModelSerializer):
    detalle = serializers.SerializerMethodField()
    ubicacion = UbicacionSerializer(required=True)
    tipopago = TipoPagoSerializer(required=True)
    tipoenvio = TipoEnvioSerializer(required=True)
    class Meta:
        model = Pedido
        fields = ['id', 'nit', 'nombre', 'telefono', 'fecha', 'cliente', 'ubicacion', 'tipopago', 'tipoenvio', 'subtotal', 'descuento', 'total', 'estado', 'detalle']
    
    def get_detalle(self, instance):
        aux_items = DetallePedido.objects.filter(pedido=instance)
        return DetallePedidoSerializer(aux_items, many=True, context=self.context).data