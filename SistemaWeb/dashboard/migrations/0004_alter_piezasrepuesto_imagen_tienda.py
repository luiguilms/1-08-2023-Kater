# Generated by Django 3.2 on 2023-08-03 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_auto_20230802_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='piezasrepuesto',
            name='imagen_tienda',
            field=models.ImageField(blank=True, null=True, upload_to='imgPiezas'),
        ),
    ]
