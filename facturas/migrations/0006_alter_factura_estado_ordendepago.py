# Generated by Django 4.2.2 on 2023-10-27 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0002_desarrollador'),
        ('facturas', '0005_codigousado_factura'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='estado',
            field=models.CharField(choices=[('Pendiente', 'Pendiente'), ('Autorizado', 'Autorizado'), ('Pagado', 'Pagado')], default='Pendiente', max_length=20),
        ),
        migrations.CreateModel(
            name='ordenDePago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('op', models.CharField(blank=True, max_length=255, null=True)),
                ('emision', models.DateField(blank=True, null=True)),
                ('alta', models.DateField(blank=True, null=True)),
                ('nroFactura', models.CharField(blank=True, max_length=255, null=True)),
                ('proveedor', models.CharField(blank=True, max_length=255, null=True)),
                ('oc', models.CharField(blank=True, max_length=255, null=True)),
                ('total', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, null=True)),
                ('ff', models.CharField(blank=True, max_length=255, null=True)),
                ('unidadEjecutora', models.CharField(blank=True, max_length=255, null=True)),
                ('objeto', models.CharField(blank=True, max_length=255, null=True)),
                ('fondoAfectado', models.CharField(blank=True, max_length=255, null=True)),
                ('codigo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administracion.codigofinanciero')),
            ],
        ),
    ]
