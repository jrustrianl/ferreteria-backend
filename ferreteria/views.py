from django.contrib.auth.hashers import make_password, check_password

from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Cliente
from .serializers import ClienteSerializer, ClienteAuthSerializer

class ClienteViewSet(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = []

    def retrieve(self, request, pk=None):
        aux_cliente = None
        try:
            aux_cliente = Cliente.objects.get(pk=pk)
        except ObjectDoesNotExist:
            content = {'message': 'No existe cliente'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ClienteSerializer(aux_cliente, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request, pk=None):
        if 'nombre' in request.data and 'email' in request.data and 'password' in request.data and 'telefono' in request.data and 'fecha_nacimiento':
            hashed_password = make_password(request.data['password'])
            try:
                new_cliente = Cliente.objects.create(nombre=request.data['nombre'], email=request.data['email'], password = hashed_password, telefono=request.data['telefono'], fecha_nacimiento=request.data['fecha_nacimiento'])
            except IntegrityError as integrity_error:
                content = {'message': str(integrity_error)}
                return Response(content, status=status.HTTP_404_NOT_FOUND)

            cliente_serializer = ClienteSerializer(new_cliente, many=False)
            return Response(cliente_serializer.data, status=status.HTTP_201_CREATED)
        else:
            content = {'message': 'Datos incompletos'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
class LoginViewSet(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = []
    
    def create(self, request, pk=None):
        if 'email' in request.data and 'password' in request.data:
            
            aux_cliente = None
            try:
                aux_cliente = Cliente.objects.get(email=request.data['email'])
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
