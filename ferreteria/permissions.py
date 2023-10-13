from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist
from .models import Cliente

class UidPermission(permissions.BasePermission):
    message = 'No tienes permisos para realizar esta acción'

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if 'userid' in request.data:
                userid = request.data['userid']
                try:
                    aux_cliente = Cliente.objects.get(pk=userid)
                    return True
                except ObjectDoesNotExist:
                    return False
            else:
                return False