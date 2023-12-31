# Generated by Django 4.2.5 on 2023-09-12 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ferreteria', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=40)),
                ('descripcion', models.CharField(max_length=255)),
                ('icono', models.ImageField(max_length=255, null=True, upload_to='CATEGORIAS')),
            ],
            options={
                'verbose_name_plural': 'categorías',
            },
        ),
        migrations.CreateModel(
            name='DetallePedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('precio', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=40)),
                ('descripcion', models.CharField(max_length=255)),
                ('icono', models.ImageField(max_length=255, null=True, upload_to='MARCAS')),
            ],
            options={
                'verbose_name_plural': 'marcas',
            },
        ),
        migrations.CreateModel(
            name='TipoEnvio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=40)),
                ('descripcion', models.CharField(blank=True, max_length=255, null=True)),
                ('monto', models.FloatField()),
            ],
            options={
                'verbose_name': 'tipo de envío',
                'verbose_name_plural': 'tipos de envío',
            },
        ),
        migrations.CreateModel(
            name='TipoPago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=40)),
                ('descripcion', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'tipo de pago',
                'verbose_name_plural': 'tipos de pago',
            },
        ),
        migrations.AlterField(
            model_name='cliente',
            name='email',
            field=models.CharField(max_length=40, unique=True, verbose_name='correo electrónico'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='estado',
            field=models.SmallIntegerField(choices=[(0, 'Disponible'), (1, 'Bloqueado'), (2, 'Eliminado')], default=0),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='fecha_nacimiento',
            field=models.DateField(verbose_name='fecha de nacimiento'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='password',
            field=models.CharField(max_length=40, verbose_name='contraseña'),
        ),
        migrations.CreateModel(
            name='Ubicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=40)),
                ('direccion', models.CharField(max_length=255)),
                ('descripcion', models.CharField(blank=True, max_length=255, null=True)),
                ('telefono', models.CharField(max_length=12)),
                ('nombre_recibe', models.CharField(blank=True, max_length=40, null=True, verbose_name='nombre quien recibe')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ubicaciones', to='ferreteria.cliente')),
            ],
            options={
                'verbose_name_plural': 'ubicaciones',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=40)),
                ('descripcion', models.TextField()),
                ('imagen', models.ImageField(max_length=255, upload_to='PRODUCTOS')),
                ('existencia', models.IntegerField()),
                ('precio', models.FloatField()),
                ('descuento', models.FloatField()),
                ('estado', models.SmallIntegerField(choices=[(0, 'Disponible'), (1, 'Pre-Venta'), (2, 'Eliminado')], default=0)),
                ('categorias', models.ManyToManyField(blank=True, to='ferreteria.categoria')),
                ('marca', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='productos', to='ferreteria.marca')),
            ],
            options={
                'verbose_name_plural': 'categorías',
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nit', models.CharField(max_length=15, verbose_name='NIT')),
                ('nombre', models.CharField(max_length=40)),
                ('telefono', models.CharField(max_length=12)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('subtotal', models.FloatField()),
                ('descuento', models.FloatField()),
                ('total', models.FloatField()),
                ('estado', models.SmallIntegerField(choices=[(0, 'Recibido'), (1, 'Procesando'), (2, 'Enviado'), (3, 'Entregado')], default=0)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedidos_cliente', to='ferreteria.cliente')),
                ('productos', models.ManyToManyField(related_name='detalles', through='ferreteria.DetallePedido', to='ferreteria.producto')),
                ('tipoenvio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedidos_tipoenvio', to='ferreteria.tipoenvio')),
                ('tipopago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedidos_tipopago', to='ferreteria.tipopago')),
                ('ubicacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedidos_ubicacion', to='ferreteria.ubicacion')),
            ],
            options={
                'verbose_name': 'Metadata Producto',
                'verbose_name_plural': 'Metadata Productos',
            },
        ),
        migrations.CreateModel(
            name='MetaProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meta_productos', to='ferreteria.producto')),
            ],
            options={
                'verbose_name': 'Metadata Producto',
                'verbose_name_plural': 'Metadata Productos',
            },
        ),
        migrations.AddField(
            model_name='detallepedido',
            name='pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles_pedido', to='ferreteria.pedido'),
        ),
        migrations.AddField(
            model_name='detallepedido',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles_producto', to='ferreteria.producto'),
        ),
        migrations.CreateModel(
            name='DetalleCarrito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carritos_cliente', to='ferreteria.cliente')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carritos_producto', to='ferreteria.producto')),
            ],
        ),
        migrations.AddField(
            model_name='cliente',
            name='carrito',
            field=models.ManyToManyField(related_name='carritos', through='ferreteria.DetalleCarrito', to='ferreteria.producto'),
        ),
    ]
