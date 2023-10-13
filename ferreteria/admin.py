import random, string

from django.contrib import admin
#from django.contrib import messages

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html

from .models import UsuarioAdmin, Producto, MetaProducto, Marca, Categoria, Cliente, Pedido, TipoEnvio, TipoMovimiento, TipoPago, Movimiento, EmpleadoProxy, DetalleCarrito, DetallePedido, UserPayment

def randomPass(lenval):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(lenval))

class UsuarioAdminInline(admin.StackedInline):
    model = UsuarioAdmin
    can_delete = False
    verbose_name_plural = 'usuarios administradores'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UsuarioAdminInline, )

class EmpleadoProxyAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'username', 'email', 'is_active')
    list_display = ('first_name', 'last_name', 'username')
    inlines = (UsuarioAdminInline, )

    def get_queryset(self, request):
        qs = super(EmpleadoProxyAdmin, self).get_queryset(request)
        return qs.filter(groups__name='Empleado')
    
    def save_model(self, request, obj, form, change):
        if change is False:
            obj.is_staff = True
            obj.set_password(obj.username)

        super().save_model(request, obj, form, change)
        
class ProductoAdminInline(admin.StackedInline):
    model = MetaProducto
    can_delete = True
    verbose_name_plural = 'metadatos'
    extra = 0

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'existencia', 'estado')
    inlines = (ProductoAdminInline, )

def descargar_recibo(obj):
    return format_html('<a target="blank" href="{0}{1}">{2}</a></th>', '/admin/ferreteria/reciboDePedido/', obj.id, 'Descargar')

descargar_recibo.allow_tags = True
descargar_recibo.short_description = "Recibo PDF"

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha', 'total', 'estado', descargar_recibo)

    def get_queryset(self, request):
        qs = super(PedidoAdmin, self).get_queryset(request)
        return qs.all().order_by('-fecha', '-id')

admin.site.site_header = 'Ferretería EL ESFUERZO'
admin.site.site_title = 'Ferretería'
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(MetaProducto)
admin.site.register(Marca)
admin.site.register(Categoria)
admin.site.register(Cliente)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(TipoEnvio)
admin.site.register(TipoMovimiento)
admin.site.register(TipoPago)
admin.site.register(Movimiento)
admin.site.register(EmpleadoProxy, EmpleadoProxyAdmin)

admin.site.register(DetalleCarrito)
admin.site.register(DetallePedido)
admin.site.register(UserPayment)