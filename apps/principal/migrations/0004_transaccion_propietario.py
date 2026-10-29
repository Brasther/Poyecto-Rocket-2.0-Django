from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def asignar_propietarios(apps, schema_editor):
    Transaccion = apps.get_model("principal", "Transaccion")
    User = apps.get_model(*settings.AUTH_USER_MODEL.split("."))
    alias = schema_editor.connection.alias

    for transaccion in Transaccion.objects.using(alias).exclude(session_id__isnull=True).iterator():
        propietario = User.objects.using(alias).filter(username=transaccion.session_id).first()
        if propietario:
            transaccion.propietario_id = propietario.pk
            transaccion.save(update_fields=["propietario"], using=alias)


class Migration(migrations.Migration):
    dependencies = [
        ("principal", "0003_codigo_seguimiento"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="transaccion",
            name="propietario",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="envios",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(asignar_propietarios, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="transaccion",
            name="session_id",
        ),
    ]
