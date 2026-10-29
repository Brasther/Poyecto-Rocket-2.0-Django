import uuid

from django.conf import settings
from django.db import models


class Transaccion(models.Model):

    ESTADO_ENVIO_CHOICES = [
        ('completado', 'Completado'),
        ('en_camino', 'En Camino'),
        ('en_proceso', 'En Proceso'),
    ]

    TIPO_PAQUETE_CHOICES = [
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
    ]

    TIPO_ENVIO_CHOICES = [
        ('normal', 'Envío Normal'),
        ('express', 'Envío Express 24hrs'),
    ]

    ID = models.AutoField(primary_key=True)
    codigo_seguimiento = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    # Datos del remitente
    nombre_remitente = models.CharField(max_length=100)
    rut_remitente = models.CharField(max_length=12)
    direccion_remitente = models.CharField(max_length=255)
    email_remitente = models.EmailField(blank=True, null=True)
    telefono_remitente = models.CharField(max_length=20, blank=True, null=True)

    # Datos del destinatario
    nombre_destinatario = models.CharField(max_length=100)
    rut_destinatario = models.CharField(max_length=12)
    direccion_destinatario = models.CharField(max_length=255)
    email_destinatario = models.EmailField(blank=True, null=True)
    telefono_destinatario = models.CharField(max_length=20, blank=True, null=True)

    # Datos del envío
    tipo_paquete = models.CharField(max_length=2, choices=TIPO_PAQUETE_CHOICES)
    tipo_envio = models.CharField(max_length=10, choices=TIPO_ENVIO_CHOICES)
    pagado = models.BooleanField(default=False)
    costo_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    propietario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="envios",
        blank=True,
        null=True,
    )

    buy_order = models.CharField(max_length=50, unique=True, blank=True, null=True)

    estado_envio = models.CharField(max_length=10, choices=ESTADO_ENVIO_CHOICES, default="en_proceso")

    def __str__(self):
        return f"Envío {self.codigo_seguimiento} ({self.get_estado_envio_display()})"


class Producto(models.Model):
    sku = models.IntegerField(primary_key=True, unique=True)
    nombre = models.CharField(max_length=50)
    stock = models.IntegerField()
    precio = models.IntegerField()
    descripcion = models.CharField(max_length=200)
    nota = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return "N° {0} - Stock: {1} - nombre: {2}".format(self.sku, self.stock, self.nombre)
