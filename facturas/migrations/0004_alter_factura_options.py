# Generated by Django 4.2.2 on 2023-10-25 20:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facturas', '0003_codigousado_codigofinanciero'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='factura',
            options={'verbose_name': 'factura', 'verbose_name_plural': 'Facturas'},
        ),
    ]
