# Generated by Django 4.2.5 on 2023-09-28 21:21

from django.db import migrations, models


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
                'verbose_name': 'Configuracion',
                'verbose_name_plural': 'Configuraciones',
            },
        ),
        migrations.CreateModel(
            name='destino',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TIPO', models.CharField(choices=[('VIVIENDA UNIFAMILIAR', 'VIVIENDA UNIFAMILIAR'), ('VIVIENDA CON COMERCIO', 'VIVIENDA CON COMERCIO'), ('VIVIENDA MULTIFAMILIAR', 'VIVIENDA MULTIFAMILIAR'), ('COMPLEJO RESIDENCIAL', 'COMPLEJO RESIDENCIAL'), ('UNIDAD FUNCIONAL HABITACIONAL', 'UNIDAD FUNCIONAL HABITACIONAL')], default=1, max_length=255)),
                ('COEFICIENTE', models.DecimalField(decimal_places=2, default=1, max_digits=10)),
            ],
            options={
                'verbose_name': 'Destino',
                'verbose_name_plural': 'Destinos',
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
                ('DESTINO', models.CharField(blank=True, choices=[('VIVIENDA UNIFAMILIAR', 'VIVIENDA UNIFAMILIAR'), ('VIVIENDA CON COMERCIO', 'VIVIENDA CON COMERCIO'), ('VIVIENDA MULTIFAMILIAR', 'VIVIENDA MULTIFAMILIAR'), ('COMPLEJO RESIDENCIAL', 'COMPLEJO RESIDENCIAL'), ('UNIDAD FUNCIONAL HABITACIONAL', 'UNIDAD FUNCIONAL HABITACIONAL')], default=1, max_length=255, null=True)),
                ('VALUACION_FISCAL', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('EMISION_ANTERIOR', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True)),
                ('DESC_CONTRIBUYENTE', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Desc. Buen Contr. (%)')),
                ('DESC_DEBITO_AUT', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Desc. Deb. Aut. (%)')),
                ('DESC_EDENOR', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('DESC_PARTIDA', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('CORREO', models.BooleanField(default=True, verbose_name='APLICA CORREO')),
            ],
            options={
                'verbose_name': 'Partida',
                'verbose_name_plural': 'Partidas',
            },
        ),
    ]