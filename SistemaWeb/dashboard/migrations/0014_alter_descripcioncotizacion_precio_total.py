# Generated by Django 3.2 on 2023-08-01 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0013_alter_descripcioncotizacion_precio_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='descripcioncotizacion',
            name='precio_total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
