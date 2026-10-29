import uuid

from django.db import migrations, models


def generar_codigos_seguimiento(apps, schema_editor):
    Transaccion = apps.get_model("principal", "Transaccion")
    for transaccion in Transaccion.objects.filter(codigo_seguimiento__isnull=True).iterator():
        transaccion.codigo_seguimiento = uuid.uuid4()
        transaccion.save(update_fields=["codigo_seguimiento"])


class Migration(migrations.Migration):
    dependencies = [
        ("principal", "0002_alter_transaccion_estado_envio"),
    ]

    operations = [
        migrations.AddField(
            model_name="transaccion",
            name="codigo_seguimiento",
            field=models.UUIDField(editable=False, null=True),
        ),
        migrations.RunPython(generar_codigos_seguimiento, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="transaccion",
            name="codigo_seguimiento",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
