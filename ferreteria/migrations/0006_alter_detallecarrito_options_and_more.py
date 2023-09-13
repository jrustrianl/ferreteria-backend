# Generated by Django 4.2.5 on 2023-09-12 23:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ferreteria', '0005_alter_metaproducto_options_alter_pedido_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='detallecarrito',
            options={'verbose_name': 'detalle de carrito', 'verbose_name_plural': 'detalles de carritos'},
        ),
        migrations.AlterModelOptions(
            name='detallemovimiento',
            options={'verbose_name': 'detalle de movimiento', 'verbose_name_plural': 'detalles de movimientos'},
        ),
        migrations.AlterModelOptions(
            name='detallepedido',
            options={'verbose_name': 'detalle de pedido', 'verbose_name_plural': 'detalles de pedidos'},
        ),
        migrations.AlterModelOptions(
            name='movimiento',
            options={'verbose_name_plural': 'movimientos'},
        ),
        migrations.AlterModelOptions(
            name='producto',
            options={'verbose_name_plural': 'productos'},
        ),
        migrations.AlterModelOptions(
            name='tipomovimiento',
            options={'verbose_name': 'tipo de movimiento', 'verbose_name_plural': 'tipos de movimiento'},
        ),
    ]