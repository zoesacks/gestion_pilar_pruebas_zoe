# Generated by Django 4.2.5 on 2023-12-05 14:25

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitudDeAyuda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('titulo', models.CharField(max_length=50)),
                ('detalle', models.TextField(blank=True, null=True)),
                ('estado', models.CharField(choices=[('Pendiente', 'Pendiente'), ('En proceso', 'En proceso'), ('Terminado', 'Terminado')], default='Pendiente', max_length=255)),
                ('desarrollador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='desarrollador', to=settings.AUTH_USER_MODEL)),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='solicitante', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Solicitud a mesa de ayuda',
                'verbose_name_plural': 'Solicitudes a mesa de ayuda',
            },
        ),
        migrations.CreateModel(
            name='FotoSolicutudDeAyuda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.ImageField(upload_to='img/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])])),
                ('solicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mesa_de_ayuda.solicituddeayuda')),
            ],
            options={
                'verbose_name': 'Foto de solicitud a mesa de ayuda',
                'verbose_name_plural': 'Fotos de solicitudes a mesa de ayuda',
            },
        ),
        migrations.CreateModel(
            name='ComentarioSolicutudDeAyuda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('solicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mesa_de_ayuda.solicituddeayuda')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Comentario de solicitud a mesa de ayuda',
                'verbose_name_plural': 'Comentarios de solicitudes a mesa de ayuda',
            },
        ),
    ]
