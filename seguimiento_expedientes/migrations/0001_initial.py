# Generated by Django 4.2.5 on 2023-11-29 19:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name': 'sector',
                'verbose_name_plural': 'Sectores',
            },
        ),
        migrations.CreateModel(
            name='TipoDocumento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField(unique=True)),
                ('descripcion', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'tipo de documento',
                'verbose_name_plural': 'Tipos de documentos',
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seguimiento_expedientes.sector')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'usuario',
                'verbose_name_plural': 'Usuarios',
            },
        ),
        migrations.CreateModel(
            name='Transferencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('fecha_confirmacion', models.DateField(blank=True, null=True)),
                ('observacion', models.TextField(blank=True, null=True)),
                ('emisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emisor', to='seguimiento_expedientes.usuario')),
                ('receptor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receptor', to='seguimiento_expedientes.usuario')),
            ],
            options={
                'verbose_name': 'transferencia',
                'verbose_name_plural': 'Transferencias',
            },
        ),
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField()),
                ('ejercicio', models.CharField(max_length=4)),
                ('fecha_alta', models.DateField(auto_now_add=True, null=True)),
                ('observacion', models.TextField(blank=True, null=True)),
                ('en_transito', models.BooleanField(default=False)),
                ('fecha_transito', models.DateField(blank=True, null=True)),
                ('destinatario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='destinatario', to='seguimiento_expedientes.usuario')),
                ('propietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='propietario', to='seguimiento_expedientes.usuario')),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seguimiento_expedientes.tipodocumento')),
                ('transferencias', models.ManyToManyField(to='seguimiento_expedientes.transferencia')),
            ],
            options={
                'verbose_name': 'documento',
                'verbose_name_plural': 'Documentos',
            },
        ),
    ]
