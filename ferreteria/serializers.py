from rest_framework import serializers

from .models import Cliente, Producto, Marca, Categoria

class ClienteAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'email', 'subtotal_carrito']

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'telefono', 'fecha_nacimiento']

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ['id', 'nombre', 'descripcion', 'icono', 'imagen_destacada']

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'icono', 'imagen_destacada']

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

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'imagen', 'precio', 'descuento', 'marca', 'categorias']