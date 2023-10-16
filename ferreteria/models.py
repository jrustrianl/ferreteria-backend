from django.db import models
from django.db.models import Lookup
from django.db.models.fields import Field

from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver


# Lookups
class LowerSearch(Lookup):
    lookup_name = 'lwsearch'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        if not params[0] is None:
            params[0] = '%' + params[0] + '%'
        return 'LOWER(%s) LIKE %s' % (lhs, rhs), params

Field.register_lookup(LowerSearch)

class EmpleadoProxy(User):
    class Meta:
        proxy = True
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"

@receiver(post_save, sender=EmpleadoProxy)
def empleadoproxy_post_save(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name="Empleado")
        instance.groups.add(group)

class UsuarioAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=12, null=True, blank=True)
    fecha_nacimiento = models.DateField(max_length=30, null=True, blank=True)
    foto = models.ImageField(max_length=255, upload_to="USUARIOS_ADMIN", null=True, blank=True)

class Marca(models.Model):
    nombre = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    imagen_destacada = models.ImageField(max_length=255, upload_to="MARCAS", null=True, blank=True)
    icono = models.ImageField(max_length=255, upload_to="MARCAS", null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "marcas"

class Categoria(models.Model):
    nombre = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    imagen_destacada = models.ImageField(max_length=255, upload_to="CATEGORIAS", null=True, blank=True)
    icono = models.ImageField(max_length=255, upload_to="CATEGORIAS", null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "categorías"

class Producto(models.Model):

    ESTADO_CHOICES = [
        (0, 'Disponible'),
        (1, 'Pre-Venta'),
        (2, 'Eliminado')
    ]

    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    miniatura = models.ImageField(max_length=255, upload_to="PRODUCTOS", null=True, blank=True)
    imagen = models.ImageField(max_length=255, upload_to="PRODUCTOS")
    imagen_destacada = models.ImageField(max_length=255, upload_to="PRODUCTOS", null=True, blank=True)
    destacado = models.BooleanField(default=False)
    mas_vendido = models.BooleanField(default=False)
    existencia = models.IntegerField()
    alerta_existencia = models.IntegerField(default=10)
    precio = models.FloatField()
    descuento = models.FloatField(null=True, blank=True)
    estado = models.SmallIntegerField(choices=ESTADO_CHOICES, default=0)
    marca = models.ForeignKey(Marca, related_name="productos", on_delete=models.SET_NULL, null=True, blank=True)
    categorias = models.ManyToManyField(Categoria)
    stripe_id = models.CharField(max_length=255, unique=True, null=True)
    stripe_id_descuento = models.CharField(max_length=255, unique=True, null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "productos"

class TipoMovimiento(models.Model):
    nombre = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "tipo de movimiento"
        verbose_name_plural = "tipos de movimiento"

class Movimiento(models.Model):

    ESTADO_CHOICES = [
        (0, 'Completado'),
        (1, 'En espera'),
        (2, 'Anulado')
    ]

    fecha = models.DateField()
    estado = models.SmallIntegerField(choices=ESTADO_CHOICES, default=0)
    usuario = models.ForeignKey(User, related_name="movimientos_usuario", on_delete=models.CASCADE)
    tipomovimiento = models.ForeignKey(TipoMovimiento, related_name="movimientos_tipo", on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, related_name='detalle_movimiento', through='DetalleMovimiento')

    class Meta:
        verbose_name_plural = "movimientos"

class DetalleMovimiento(models.Model):
    cantidad = models.IntegerField()
    movimiento = models.ForeignKey(Movimiento, related_name='detalle_movimiento_movimiento', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, related_name='detalle_movimiento_producto', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "detalle de movimiento"
        verbose_name_plural = "detalles de movimientos"

class Cliente(models.Model):

    ESTADO_CHOICES = [
        (0, 'Disponible'),
        (1, 'Bloqueado'),
        (2, 'Eliminado')
    ]

    nombre = models.CharField(max_length=40)
    email = models.CharField(verbose_name="correo electrónico", max_length=40, unique=True)
    password = models.CharField(verbose_name="contraseña", max_length=255)
    telefono = models.CharField(max_length=12)
    fecha_nacimiento = models.DateField(verbose_name="fecha de nacimiento")
    subtotal_carrito = models.FloatField(default=0)
    estado = models.SmallIntegerField(choices=ESTADO_CHOICES, default=0)
    carrito = models.ManyToManyField(Producto, related_name='carritos', through='DetalleCarrito')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "clientes"

class Ubicacion(models.Model):
    
    ESTADO_CHOICES = [
        (0, 'Disponible'),
        (1, 'Eliminado')
    ]

    nombre = models.CharField(max_length=40)
    direccion = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    telefono = models.CharField(max_length=12)
    nombre_recibe = models.CharField(verbose_name="nombre quien recibe", max_length=40, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, related_name='ubicaciones', on_delete=models.CASCADE)
    estado = models.SmallIntegerField(choices=ESTADO_CHOICES, default=0)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "ubicaciones"

'''class MetodoPago(models.Model):
    titular = models.CharField(max_length=255)
    num_tarjeta = models.CharField(max_length=255)
    fecha_caducidad = models.CharField(max_length=255)
    cliente = models.ForeignKey(Cliente, related_name='metodos_pago', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "método de pago"
        verbose_name_plural = "métodos de pago"'''

class TipoEnvio(models.Model):
    nombre = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    monto = models.FloatField()
    stripe_id = models.CharField(max_length=255, unique=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "tipo de envío"
        verbose_name_plural = "tipos de envío"

class TipoPago(models.Model):
    nombre = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "tipo de pago"
        verbose_name_plural = "tipos de pago"

class MetaProducto(models.Model):
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    producto = models.ForeignKey(Producto, related_name="meta_productos", on_delete=models.CASCADE)

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = "metadata producto"
        verbose_name_plural = "metadata productos"

class Pedido(models.Model):

    ESTADO_CHOICES = [
        (0, 'Recibido'),
        (1, 'Procesando'),
        (2, 'Pendiente de pago'),
        (3, 'Enviado'),
        (4, 'Entregado')
    ]

    nit = models.CharField(max_length=15, verbose_name="NIT")
    nombre = models.CharField(max_length=40)
    telefono = models.CharField(max_length=12)
    fecha = models.DateField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente, related_name="pedidos_cliente", on_delete=models.CASCADE)
    ubicacion = models.ForeignKey(Ubicacion, related_name="pedidos_ubicacion", on_delete=models.CASCADE)
    tipopago = models.ForeignKey(TipoPago, related_name="pedidos_tipopago", on_delete=models.CASCADE)
    tipoenvio = models.ForeignKey(TipoEnvio, related_name="pedidos_tipoenvio", on_delete=models.CASCADE, null=True, blank=True)
    subtotal = models.FloatField()
    descuento = models.FloatField(null=True, blank=True)
    total = models.FloatField()
    estado = models.SmallIntegerField(choices=ESTADO_CHOICES, default=0)
    productos = models.ManyToManyField(Producto, related_name='detalle_pedido', through='DetallePedido')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "pedidos"

class DetallePedido(models.Model):
    cantidad = models.IntegerField()
    precio = models.FloatField()
    pedido = models.ForeignKey(Pedido, related_name='detalle_pedido_pedido', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, related_name='detalle_pedido_producto', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "detalle de pedido"
        verbose_name_plural = "detalles de pedidos"

class DetalleCarrito(models.Model):
    cantidad = models.IntegerField()
    cliente = models.ForeignKey(Cliente, related_name='carritos_cliente', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, related_name='carritos_producto', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "detalle de carrito"
        verbose_name_plural = "detalles de carritos"

class UserPayment(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    payment_bool = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=500)