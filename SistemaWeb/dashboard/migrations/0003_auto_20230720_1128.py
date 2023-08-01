# Generated by Django 3.2 on 2023-07-20 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_cliente_direccion_moneda_pago_proforma_vendedor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bu', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='cliente',
            name='obs',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='moneda',
            name='tipo',
            field=models.CharField(choices=[('soles', 'Soles'), ('dolares', 'Dolares')], max_length=20),
        ),
        migrations.AlterField(
            model_name='proforma',
            name='fecha',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='proforma',
            name='bu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.bu'),
        ),
    ]
