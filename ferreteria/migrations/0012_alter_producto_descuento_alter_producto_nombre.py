# Generated by Django 4.2.5 on 2023-10-11 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ferreteria', '0011_alter_producto_descuento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='descuento',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='nombre',
            field=models.CharField(max_length=150),
        ),
    ]
