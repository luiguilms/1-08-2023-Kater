# Generated by Django 3.2 on 2023-08-01 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_alter_descripcioncotizacion_codigo'),
    ]

    operations = [
        migrations.AddField(
            model_name='descripcioncotizacion',
            name='descuento',
            field=models.IntegerField(blank=True, choices=[(5, '5%'), (10, '10%'), (15, '15%')], default=None, null=True),
        ),
    ]
