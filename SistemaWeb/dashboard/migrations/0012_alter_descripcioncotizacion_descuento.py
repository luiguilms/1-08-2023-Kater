# Generated by Django 3.2 on 2023-08-01 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_descripcioncotizacion_descuento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='descripcioncotizacion',
            name='descuento',
            field=models.IntegerField(choices=[(0, 'Sin descuento'), (5, '5%'), (10, '10%'), (15, '15%')], default=0),
        ),
    ]
