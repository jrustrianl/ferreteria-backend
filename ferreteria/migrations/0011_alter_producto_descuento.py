# Generated by Django 4.2.5 on 2023-10-11 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ferreteria', '0010_empleadoproxy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='descuento',
            field=models.FloatField(null=True),
        ),
    ]