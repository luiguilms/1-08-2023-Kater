# Generated by Django 3.2 on 2023-08-04 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_cotizacionconsultoria_cotizacionmanodeobra_descripcioncotizacionconsultoria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='descripcioncotizacionconsultoria',
            name='codigo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.consultoria'),
        ),
        migrations.AlterField(
            model_name='descripcioncotizacionconsultoria',
            name='cotizacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.cotizacionconsultoria'),
        ),
        migrations.CreateModel(
            name='descripcionCotizacionManoDeObra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('descripcion', models.CharField(blank=True, max_length=1000)),
                ('precio_unitario', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('disponibilidad', models.CharField(max_length=20)),
                ('precio_total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('descuento', models.IntegerField(choices=[(0, 'Sin descuento'), (5, '5%'), (10, '10%'), (15, '15%')], default=0)),
                ('codigo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.manodeobra')),
                ('cotizacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.cotizacionmanodeobra')),
            ],
        ),
    ]
