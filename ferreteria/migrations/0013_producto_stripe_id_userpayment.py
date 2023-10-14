# Generated by Django 4.2.5 on 2023-10-12 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ferreteria', '0012_alter_producto_descuento_alter_producto_nombre'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='stripe_id',
            field=models.CharField(max_length=255, unique=True, null=True),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='UserPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_bool', models.BooleanField(default=False)),
                ('stripe_checkout_id', models.CharField(max_length=500)),
                ('app_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ferreteria.cliente')),
            ],
        ),
    ]