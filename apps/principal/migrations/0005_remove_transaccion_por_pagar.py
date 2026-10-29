from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("principal", "0004_transaccion_propietario"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="transaccion",
            name="por_pagar",
        ),
    ]
