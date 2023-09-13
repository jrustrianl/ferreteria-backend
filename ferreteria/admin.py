from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import UsuarioAdmin, Producto, MetaProducto, Marca, Categoria, Cliente, Pedido, TipoEnvio, TipoMovimiento, TipoPago, Movimiento

class UsuarioAdminInline(admin.StackedInline):
    model = UsuarioAdmin
    can_delete = False
    verbose_name_plural = 'usuarios administradores'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UsuarioAdminInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Producto)
admin.site.register(MetaProducto)
admin.site.register(Marca)
admin.site.register(Categoria)
admin.site.register(Cliente)
admin.site.register(Pedido)
admin.site.register(TipoEnvio)
admin.site.register(TipoMovimiento)
admin.site.register(TipoPago)
admin.site.register(Movimiento)