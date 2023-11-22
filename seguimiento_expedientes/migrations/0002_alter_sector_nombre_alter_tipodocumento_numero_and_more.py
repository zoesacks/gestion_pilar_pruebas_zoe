# Generated by Django 4.2.2 on 2023-11-16 15:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('seguimiento_expedientes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sector',
            name='nombre',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='tipodocumento',
            name='numero',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]