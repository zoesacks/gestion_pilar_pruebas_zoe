# Generated by Django 4.2.2 on 2023-11-07 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturas', '0007_alter_factura_autorizado_alter_factura_devengado'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordendepago',
            name='pagado',
            field=models.BooleanField(default=False),
        ),
    ]