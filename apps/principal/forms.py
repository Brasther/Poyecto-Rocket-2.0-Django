from django import forms

from .models import Transaccion


REGIONES = [
    ("1", "Arica y Parinacota"),
    ("2", "Tarapacá"),
    ("3", "Antofagasta"),
    ("4", "Atacama"),
    ("5", "Coquimbo"),
    ("6", "Valparaíso"),
    ("7", "Metropolitana de Santiago"),
    ("8", "Libertador General Bernardo O'Higgins"),
    ("9", "Maule"),
    ("10", "Ñuble"),
    ("11", "Biobío"),
    ("12", "La Araucanía"),
    ("13", "Los Ríos"),
    ("14", "Los Lagos"),
    ("15", "Aysén del General Carlos Ibáñez del Campo"),
    ("16", "Magallanes y de la Antártica Chilena"),
]


class CrearEnvioForm(forms.Form):
    nombreRemitente = forms.CharField(label="Nombre del remitente", max_length=100)
    rutRemitente = forms.CharField(label="RUT del remitente", max_length=12)
    direccionRemitente = forms.CharField(label="Dirección del remitente", max_length=255)
    Email = forms.EmailField(label="Correo del remitente", required=False)
    telefonoRemitente = forms.CharField(label="Teléfono del remitente", max_length=20, required=False)
    nombreDestinatario = forms.CharField(label="Nombre del destinatario", max_length=100)
    rutDestinatario = forms.CharField(label="RUT del destinatario", max_length=12)
    direccionDestinatario = forms.CharField(label="Dirección del destinatario", max_length=255)
    emailDestinatario = forms.EmailField(label="Correo del destinatario", required=False)
    region = forms.ChoiceField(label="Región de destino", choices=REGIONES)
    comuna = forms.CharField(label="Comuna de destino", max_length=80)
    telefonoDestinatario = forms.CharField(label="Teléfono del destinatario", max_length=20, required=False)
    tipoPaquete = forms.ChoiceField(label="Tamaño del paquete", choices=Transaccion.TIPO_PAQUETE_CHOICES)
    tipoEnvio = forms.ChoiceField(label="Tipo de envío", choices=Transaccion.TIPO_ENVIO_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            control_class = "form-select" if isinstance(field, forms.ChoiceField) else "form-control"
            field.widget.attrs.update({"class": control_class})


class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = (
            "nombre_remitente",
            "rut_remitente",
            "direccion_remitente",
            "email_remitente",
            "telefono_remitente",
            "nombre_destinatario",
            "rut_destinatario",
            "direccion_destinatario",
            "email_destinatario",
            "telefono_destinatario",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


