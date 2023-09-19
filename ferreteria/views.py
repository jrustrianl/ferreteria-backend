from django.contrib.auth.hashers import make_password, check_password

from django.db import IntegrityError, DataError
from django.core.exceptions import ObjectDoesNotExist, ValidationError

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
