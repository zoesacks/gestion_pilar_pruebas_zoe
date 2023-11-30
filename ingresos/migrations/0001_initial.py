# Generated by Django 4.2.5 on 2023-11-29 19:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='regimen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NUMERO', models.IntegerField()),
                ('INCISO', models.CharField(blank=True, max_length=2, null=True)),
                ('DESCRIPCION', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Regimen',
                'verbose_name_plural': 'Tabla de regímenes',
            },
        ),
        migrations.CreateModel(
            name='tabla_alicuotas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CODIGO', models.CharField(max_length=15)),
                ('BASE_DESDE', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('BASE_HASTA', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('MONTO_FIJO', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('ALICUOTA_REAL', models.DecimalField(decimal_places=4, max_digits=4)),
                ('ALICUOTA_PROYECTADA', models.DecimalField(blank=True, decimal_places=4, max_digits=4, null=True)),
                ('REGIMEN', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ingresos.regimen')),
            ],
            options={
                'verbose_name': 'Alicuota',
                'verbose_name_plural': 'Tabla de alícuotas',
            },
        ),
        migrations.CreateModel(
            name='base_contribuyentes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CUENTA', models.IntegerField()),
                ('TITULAR', models.CharField(max_length=255)),
                ('BASE', models.DecimalField(decimal_places=2, max_digits=20)),
                ('REGIMEN', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ingresos.regimen')),
            ],
            options={
                'verbose_name': 'Contribuyente',
                'verbose_name_plural': 'Base de contribuyentes',
            },
        ),
    ]
