# Generated by Django 4.2.5 on 2023-09-15 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ferreteria', '0006_alter_detallecarrito_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='subtotal_carrito',
            field=models.FloatField(null=True),
        ),
    ]