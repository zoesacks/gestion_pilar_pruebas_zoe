# Generated by Django 4.2.2 on 2023-11-15 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='configuracion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EJERCICIO', models.IntegerField(default=2023)),
                ('MES', models.CharField(choices=[('01', 'ENERO'), ('02', 'FEBRERO'), ('03', 'MARZO'), ('04', 'ABRIL'), ('05', 'MAYO'), ('06', 'JUNIO'), ('07', 'JULIO'), ('08', 'AGOSTO'), ('09', 'SEPTIEMBRE'), ('10', 'OCTUBRE'), ('11', 'NOVIEMBRE'), ('12', 'DICIEMBRE')], default=1, max_length=255)),
                ('ALICUOTA', models.DecimalField(blank=True, decimal_places=4, max_digits=15, null=True)),
                ('MODULO', models.DecimalField(blank=True, decimal_places=4, max_digits=15, null=True)),
                ('BOMBERO', models.DecimalField(decimal_places=2, max_digits=15)),
                ('CORREO', models.DecimalField(decimal_places=2, max_digits=15)),
                ('ALICUOTA_PROYECTADA', models.DecimalField(blank=True, decimal_places=4, max_digits=15, null=True)),
            ],
            options={
                'verbose_name': 'periodo',
                'verbose_name_plural': 'Conf. por periodo',
            },
        ),
        migrations.CreateModel(
            name='destino',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NUM_ORDENANZA', models.IntegerField()),
                ('ID_SISTEMA', models.IntegerField()),
                ('DESCRIPCION', models.CharField(max_length=255)),
                ('COEFICIENTE', models.DecimalField(decimal_places=2, default=1, max_digits=10)),
                ('MINIMO', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('EXCLUYE_FONDO', models.BooleanField(default=False, verbose_name='Excluye sub-tasa por Fondo Educativo')),
            ],
            options={
                'verbose_name': 'Destino',
                'verbose_name_plural': 'Tabla de destinos',
            },
        ),
        migrations.CreateModel(
            name='destinoFondo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DESCRIPCION', models.CharField(max_length=255)),
                ('MODULO', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
            options={
                'verbose_name': 'destino de fondo educativo',
                'verbose_name_plural': 'Config. Destinos fondo edu.',
            },
        ),
        migrations.CreateModel(
            name='partida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PARTIDA', models.IntegerField(unique=True)),
                ('EJERCICIO', models.IntegerField(default=2023)),
                ('MES', models.CharField(choices=[('01', 'ENERO'), ('02', 'FEBRERO'), ('03', 'MARZO'), ('04', 'ABRIL'), ('05', 'MAYO'), ('06', 'JUNIO'), ('07', 'JULIO'), ('08', 'AGOSTO'), ('09', 'SEPTIEMBRE'), ('10', 'OCTUBRE'), ('11', 'NOVIEMBRE'), ('12', 'DICIEMBRE')], default=1, max_length=255)),
                ('TITULAR', models.CharField(max_length=255)),
                ('CARACTERISTICA', models.CharField(choices=[('ABIERTO', 'ABIERTO'), ('COUNTRY', 'COUNTRY')], default=1, max_length=255)),
                ('BARRIO', models.CharField(blank=True, max_length=255, null=True)),
                ('VALUACION_FISCAL', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('EMISION_ANTERIOR', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True)),
                ('DESC_CONTRIBUYENTE', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Desc. Buen Contr.)')),
                ('DESC_DEBITO_AUT', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Desc. Deb. Aut.')),
                ('DESC_EDENOR', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('DESC_PARTIDA', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('CORREO', models.BooleanField(default=True, verbose_name='APLICA CORREO')),
                ('DESTINO', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='servicios_generales.destino')),
            ],
            options={
                'verbose_name': 'tasa',
                'verbose_name_plural': 'Base de tasas',
            },
        ),
        migrations.AddField(
            model_name='destino',
            name='DESTINO_FONDO',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='servicios_generales.destinofondo'),
        ),
    ]
