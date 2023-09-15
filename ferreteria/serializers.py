from rest_framework import serializers

from .models import Cliente

class ClienteAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'email', 'subtotal_carrito']

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'telefono', 'fecha_nacimiento']