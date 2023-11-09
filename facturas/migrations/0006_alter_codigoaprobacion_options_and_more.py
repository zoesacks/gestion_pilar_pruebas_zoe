# Generated by Django 4.2.2 on 2023-11-03 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0002_desarrollador'),
        ('facturas', '0005_alter_factura_codigo_alter_factura_devengado_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='codigoaprobacion',
            options={'verbose_name': 'codigo de aprobacion', 'verbose_name_plural': 'Codigos de aprobacion'},
        ),
        migrations.AlterModelOptions(
            name='codigousado',
            options={'verbose_name': 'codigo de usado', 'verbose_name_plural': 'Codigos de usados'},
        ),
        migrations.AlterModelOptions(
            name='ordendepago',
            options={'verbose_name': 'orden de pago', 'verbose_name_plural': 'Ordenes de pago'},
        ),
        migrations.RenameField(
            model_name='factura',
            old_name='fondoAfectado',
            new_name='fondo_afectado',
        ),
        migrations.RenameField(
            model_name='factura',
            old_name='nroFactura',
            new_name='nro_factura',
        ),
        migrations.RenameField(
            model_name='factura',
            old_name='unidadEjecutora',
            new_name='unidad_ejecutora',
        ),
        migrations.RemoveField(
            model_name='codigoaprobacion',
            name='codigoApro',
        ),
        migrations.RemoveField(
            model_name='codigousado',
            name='codigoFinanciero',
        ),
        migrations.RemoveField(
            model_name='codigousado',
            name='montoUsado',
        ),
        migrations.RemoveField(
            model_name='ordendepago',
            name='nroFactura',
        ),
        migrations.AddField(
            model_name='codigoaprobacion',
            name='codigo_apro',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='codigousado',
            name='codigo_financiero',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='administracion.codigofinanciero'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='codigousado',
            name='monto_usado',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15),
        ),
        migrations.AddField(
            model_name='ordendepago',
            name='nro_factura',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='codigoaprobacion',
            name='monto',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='codigousado',
            name='codigo',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='facturas.codigoaprobacion'),
        ),
        migrations.AlterField(
            model_name='codigousado',
            name='factura',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='facturas.factura'),
        ),
        migrations.AlterField(
            model_name='codigousado',
            name='fecha',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='codigousado',
            name='usuario',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='ordendepago',
            name='op',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='ordendepago',
            name='proveedor',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='ordendepago',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=25),
        ),
    ]