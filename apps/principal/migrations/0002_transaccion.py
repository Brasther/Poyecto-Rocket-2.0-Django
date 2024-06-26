# Generated by Django 5.0.1 on 2024-05-23 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_remitente', models.CharField(max_length=100)),
                ('rut_remitente', models.CharField(max_length=12)),
                ('direccion_remitente', models.CharField(max_length=255)),
                ('email_remitente', models.EmailField(blank=True, max_length=254, null=True)),
                ('telefono_remitente', models.CharField(blank=True, max_length=20, null=True)),
                ('nombre_destinatario', models.CharField(max_length=100)),
                ('rut_destinatario', models.CharField(max_length=12)),
                ('direccion_destinatario', models.CharField(max_length=255)),
                ('email_destinatario', models.EmailField(blank=True, max_length=254, null=True)),
                ('telefono_destinatario', models.CharField(blank=True, max_length=20, null=True)),
                ('tipo_paquete', models.CharField(choices=[('xs', 'XS'), ('s', 'S'), ('m', 'M'), ('l', 'L'), ('xl', 'XL')], max_length=2)),
                ('tipo_envio', models.CharField(choices=[('normal', 'Envío Normal'), ('express', 'Envío Express 24hrs')], max_length=10)),
                ('pagado', models.BooleanField(default=False)),
                ('por_pagar', models.BooleanField(default=False)),
                ('costo_total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
        ),
    ]
