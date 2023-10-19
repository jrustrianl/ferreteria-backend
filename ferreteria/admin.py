import random, string

from django import forms
from django.shortcuts import redirect
from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from django.utils.html import format_html

from .models import UsuarioAdmin, Producto, MetaProducto, Marca, Categoria, Cliente, Pedido, TipoEnvio, TipoMovimiento, TipoPago, Movimiento, EmpleadoProxy, DetalleCarrito, DetallePedido, DetalleMovimiento, UserPayment

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

class NewProductoForm(forms.ModelForm):

    inicio_existencia = forms.IntegerField()

    def save(self, commit=True):
        primer_existencia = self.cleaned_data.get('inicio_existencia', None)
        self.instance.existencia = primer_existencia
        return super(NewProductoForm, self).save(commit=commit)

    class Meta:
        model = Producto
        exclude = ["existencia"]

class EmpleadoProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "descripcion", "miniatura", "imagen", "destacado", "mas_vendido"]

def alerta_baja_existencia(obj):
    return "Sí" if obj.existencia <= obj.alerta_existencia else "No"

alerta_baja_existencia.short_description = "Baja existencia"
alerta_baja_existencia.admin_order_field = "existencia"

class ProductoAdmin(admin.ModelAdmin):
    add_form = NewProductoForm
    empleado_form = EmpleadoProductoForm
    exclude = ["existencia"]
    list_display = ('nombre', 'existencia', 'estado', alerta_baja_existencia)
    inlines = (ProductoAdminInline, )

    def get_queryset(self, request):
        qs = super(ProductoAdmin, self).get_queryset(request)
        return qs.all().order_by('nombre')
    
    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults["form"] = self.add_form
        else:
            if request.user.groups.filter(name='Empleado').exists():
                defaults["form"] = self.empleado_form
        defaults.update(kwargs)
        form = super(ProductoAdmin, self).get_form(request, obj, **defaults)
        form.current_user = request.user
        return form
    
    def response_add(self, request, obj, post_url_continue=None):
        tipo_mov = TipoMovimiento.objects.get(nombre__exact="Nuevo producto")
        movimiento = Movimiento.objects.create(usuario=request.user, tipomovimiento=tipo_mov, descripcion="Se añadió un nuevo producto (" + obj.nombre + ") al catálogo.")
        DetalleMovimiento.objects.create(cantidad=obj.existencia, movimiento=movimiento, producto=obj)
        messages.success(request, 'El producto se añadió correctamente.')
        return redirect('/admin/ferreteria/producto')

def descargar_recibo(obj):
    return format_html('<a target="blank" href="{0}{1}">{2}</a></th>', '/admin/ferreteria/reciboDePedido/', obj.id, 'Descargar')

descargar_recibo.allow_tags = True
descargar_recibo.short_description = "Recibo PDF"

class DetallePedidoAdminInline(admin.StackedInline):
    model = DetallePedido
    can_delete = False
    verbose_name_plural = 'detalle'
    extra = 0

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha', 'total', 'estado', descargar_recibo)
    inlines = (DetallePedidoAdminInline,)

    def get_queryset(self, request):
        qs = super(PedidoAdmin, self).get_queryset(request)
        return qs.all().order_by('-fecha', '-id')
    
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono', 'estado')
    search_fields = ('nombre', 'email')

    def get_queryset(self, request):
        qs = super(ClienteAdmin, self).get_queryset(request)
        return qs.all().order_by('estado', 'nombre')
    
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'icono')
    search_fields = ('nombre',)

    def get_queryset(self, request):
        qs = super(MarcaAdmin, self).get_queryset(request)
        return qs.all().order_by('nombre')

def preview_icono(obj):
    return format_html('<img style="width: 150px; height: 150px" src="{0}"/>', obj.icono.path)

preview_icono.allow_tags = True
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', preview_icono)
    search_fields = ('nombre',)

    def get_queryset(self, request):
        qs = super(CategoriaAdmin, self).get_queryset(request)
        return qs.all().order_by('nombre')

class DetalleMovimientoForm(forms.ModelForm):
    class Meta:
        model = DetalleMovimiento
        fields = '__all__'

    def clean(self):
        mov = self.cleaned_data.get('movimiento')
        if mov.tipomovimiento.nombre == 'Salida de producto':
            prod = self.cleaned_data.get('producto')
            if prod.existencia <= self.cleaned_data.get('cantidad'):
                raise forms.ValidationError("Si es salida de producto, cantidad no puede ser mayor o igual que la existencia actual.")
        return self.cleaned_data

class MovimientoAdminInline(admin.StackedInline):
    model = DetalleMovimiento
    can_delete = False
    verbose_name_plural = 'detalles'
    extra = 0
    form = DetalleMovimientoForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "producto":
            kwargs["queryset"] = Producto.objects.all().order_by('nombre')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class MovimientoAdmin(admin.ModelAdmin):
    fields = ('descripcion', 'tipomovimiento')
    list_display = ('tipomovimiento', 'usuario', 'fecha')
    search_fields = ('fecha',)
    inlines = (MovimientoAdminInline, )

    def get_queryset(self, request):
        qs = super(MovimientoAdmin, self).get_queryset(request)
        return qs.all().order_by('-fecha')
    
    def save_model(self, request, obj, form, change):
        obj.usuario = request.user
        super().save_model(request, obj, form, change)

admin.site.site_header = 'Ferretería EL ESFUERZO'
admin.site.site_title = 'Ferretería'
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Producto, ProductoAdmin)
#admin.site.register(MetaProducto)
admin.site.register(Marca, MarcaAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(TipoEnvio)
admin.site.register(TipoMovimiento)
admin.site.register(TipoPago)
admin.site.register(Movimiento, MovimientoAdmin)
#admin.site.register(DetalleMovimiento)
admin.site.register(EmpleadoProxy, EmpleadoProxyAdmin)

#admin.site.register(DetalleCarrito)
#admin.site.register(DetallePedido)
admin.site.register(UserPayment)