# Generated by Django 4.2.5 on 2023-12-05 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mesa_de_ayuda', '0003_rename_cometarios_solicituddeayuda_comentarios'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicituddeayuda',
            name='comentarios',
        ),
        migrations.RemoveField(
            model_name='solicituddeayuda',
            name='fotos',
        ),
        migrations.AddField(
            model_name='solicituddeayuda',
            name='comentarios',
            field=models.ManyToManyField(to='mesa_de_ayuda.comentariosolicutuddeayuda'),
        ),
        migrations.AddField(
            model_name='solicituddeayuda',
            name='fotos',
            field=models.ManyToManyField(to='mesa_de_ayuda.fotosolicutuddeayuda'),
        ),
    ]