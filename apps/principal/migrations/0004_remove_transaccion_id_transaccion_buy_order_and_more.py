# Generated by Django 5.0.1 on 2024-05-23 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0003_alter_transaccion_costo_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaccion',
            name='id',
        ),
        migrations.AddField(
            model_name='transaccion',
            name='buy_order',
            field=models.CharField(default=0.0, max_length=20),
        ),
        migrations.AddField(
            model_name='transaccion',
            name='session_id',
            field=models.CharField(default=0.0, max_length=20),
        ),
        migrations.AddField(
            model_name='transaccion',
            name='ID',
            field=models.IntegerField(default=0.0, primary_key=True, serialize=False, unique=True),
        ),
    ]
