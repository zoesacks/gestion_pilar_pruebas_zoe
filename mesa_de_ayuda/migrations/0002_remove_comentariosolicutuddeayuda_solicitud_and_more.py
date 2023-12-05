# Generated by Django 4.2.5 on 2023-12-05 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mesa_de_ayuda', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comentariosolicutuddeayuda',
            name='solicitud',
        ),
        migrations.RemoveField(
            model_name='fotosolicutuddeayuda',
            name='solicitud',
        ),
        migrations.AddField(
            model_name='solicituddeayuda',
            name='cometarios',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mesa_de_ayuda.comentariosolicutuddeayuda'),
        ),
        migrations.AddField(
            model_name='solicituddeayuda',
            name='fotos',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mesa_de_ayuda.fotosolicutuddeayuda'),
        ),
    ]