import uuid
from decimal import Decimal, InvalidOperation

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST
from transbank.common.integration_api_keys import IntegrationApiKeys
from transbank.common.integration_commerce_codes import IntegrationCommerceCodes
from transbank.common.integration_type import IntegrationType
from transbank.common.options import WebpayOptions
from transbank.error.transbank_error import TransbankError
from transbank.webpay.webpay_plus.transaction import Transaction

from .forms import CrearEnvioForm, REGIONES, TransaccionForm
from .models import Transaccion
from .pricing import calcular_costo_envio


def obtener_transaccion_transbank():
    configuracion = settings.TRANSBANK
    entorno = configuracion["INTEGRATION_TYPE"]
    if entorno not in {"TEST", "LIVE"}:
        raise ImproperlyConfigured("TRANSBANK_INTEGRATION_TYPE debe ser TEST o LIVE.")

    if entorno == "TEST":
        codigo_comercio = configuracion["COMMERCE_CODE"] or IntegrationCommerceCodes.WEBPAY_PLUS
        api_key = configuracion["API_KEY"] or IntegrationApiKeys.WEBPAY
    else:
        codigo_comercio = configuracion["COMMERCE_CODE"]
        api_key = configuracion["API_KEY"]
        if not codigo_comercio or not api_key:
            raise ImproperlyConfigured(
                "Define TRANSBANK_COMMERCE_CODE y TRANSBANK_API_KEY para usar el entorno LIVE."
            )

    opciones = WebpayOptions(codigo_comercio, api_key, IntegrationType[entorno])
    return Transaction(opciones)


def cargarInicio(request):
    return render(request, "inicio.html")


def cargarQuienesSomos(request):
    return render(request, "quienesSomos.html")


def cargarPoweredBy(request):
    return render(request, "poweredby.html")


def cargarTerminosYcondiciones(request):
    return render(request, "terminosYcon.html")


def signup(request):
    form = UserCreationForm(request.POST or None)
    for field in form.fields.values():
        field.widget.attrs["class"] = "form-control"
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Tu cuenta quedó creada.")
        return redirect("home")
    return render(request, "signup.html", {"form": form})


def signin(request):
    form = AuthenticationForm(request, data=request.POST or None)
    for field in form.fields.values():
        field.widget.attrs["class"] = "form-control"
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("home")
    return render(request, "signin.html", {"form": form})


@login_required
@require_POST
def signout(request):
    logout(request)
    return redirect("home")


@login_required
def formulario(request):
    return render(request, "formulario.html", {"form": CrearEnvioForm()})


@permission_required("principal.view_transaccion", raise_exception=True)
def cargarTransaccion(request):
    transacciones = Transaccion.objects.order_by("-ID")
    return render(request, "cargar_transaccion.html", {"transacciones": transacciones})


def _envios_editables_por(request):
    if request.user.has_perm("principal.change_transaccion"):
        return Transaccion.objects.all()
    return Transaccion.objects.filter(propietario=request.user)


@login_required
def editar_transaccion(request, transaccion_id):
    transaccion = get_object_or_404(_envios_editables_por(request), ID=transaccion_id)
    if transaccion.pagado and not request.user.has_perm("principal.change_transaccion"):
        messages.error(request, "No se puede editar un envío que ya tiene un pago confirmado.")
        return redirect("mis_transacciones")

    form = TransaccionForm(request.POST or None, instance=transaccion)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Los datos del envío se actualizaron.")
        return redirect("mis_transacciones")
    return render(request, "editar_transaccion.html", {"form": form, "transaccion": transaccion})


@login_required
@require_POST
def eliminar_transaccion(request, transaccion_id):
    if request.user.has_perm("principal.delete_transaccion"):
        transaccion = get_object_or_404(Transaccion, ID=transaccion_id)
    else:
        transaccion = get_object_or_404(
            Transaccion, ID=transaccion_id, propietario=request.user
        )
        if transaccion.pagado:
            messages.error(request, "No se puede eliminar un envío que ya tiene un pago confirmado.")
            return redirect("mis_transacciones")

    transaccion.delete()
    messages.success(request, "El envío se eliminó.")
    return redirect("mis_transacciones")


@permission_required("principal.change_transaccion", raise_exception=True)
@require_POST
def editar_estado_envio(request, transaccion_id):
    nuevo_estado = request.POST.get("estado_envio")
    estados_validos = {valor for valor, _ in Transaccion.ESTADO_ENVIO_CHOICES}
    if nuevo_estado not in estados_validos:
        return HttpResponseBadRequest("El estado indicado no es válido.")

    transaccion = get_object_or_404(Transaccion, ID=transaccion_id)
    transaccion.estado_envio = nuevo_estado
    transaccion.save(update_fields=["estado_envio"])
    messages.success(request, "El estado del envío se actualizó.")
    return redirect("cargarTransaccion")


@login_required
@require_POST
def iniciar_transaccion(request):
    form = CrearEnvioForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Revisa los datos del formulario e inténtalo de nuevo.")
        return render(request, "formulario.html", {"form": form})

    datos = form.cleaned_data
    try:
        costo_total = calcular_costo_envio(
            datos["tipoPaquete"], datos["region"], datos["tipoEnvio"]
        )
    except ValueError as error:
        form.add_error(None, str(error))
        return render(request, "formulario.html", {"form": form})

    nombre_region = dict(REGIONES)[datos["region"]]
    direccion_destinatario = ", ".join(
        (datos["direccionDestinatario"], datos["comuna"], nombre_region, "Chile")
    )
    buy_order = uuid.uuid4().hex[:26]
    transaccion = Transaccion.objects.create(
        nombre_remitente=datos["nombreRemitente"],
        rut_remitente=datos["rutRemitente"],
        direccion_remitente=datos["direccionRemitente"],
        email_remitente=datos["Email"] or None,
        telefono_remitente=datos["telefonoRemitente"] or None,
        nombre_destinatario=datos["nombreDestinatario"],
        rut_destinatario=datos["rutDestinatario"],
        direccion_destinatario=direccion_destinatario,
        email_destinatario=datos["emailDestinatario"] or None,
        telefono_destinatario=datos["telefonoDestinatario"] or None,
        tipo_paquete=datos["tipoPaquete"],
        tipo_envio=datos["tipoEnvio"],
        pagado=False,
        costo_total=costo_total,
        propietario=request.user,
        buy_order=buy_order,
    )

    return_url = request.build_absolute_uri("/transbank/completar-transaccion/")
    try:
        respuesta = obtener_transaccion_transbank().create(
            buy_order, str(request.user.pk), int(costo_total), return_url
        )
    except TransbankError:
        messages.error(request, "No se pudo iniciar el pago de prueba. Puedes conservar este envío y volver a intentarlo más tarde.")
        return redirect("mis_transacciones")

    if respuesta.get("token") and respuesta.get("url"):
        return redirect(f"{respuesta['url']}?token_ws={respuesta['token']}")

    messages.error(request, "Transbank no devolvió una sesión de pago válida.")
    return redirect("mis_transacciones")


@require_GET
def completar_transaccion(request):
    token_ws = request.GET.get("token_ws")
    if not token_ws:
        return render(request, "error.html", {"message": "No se recibió el token de pago."})

    try:
        respuesta = obtener_transaccion_transbank().commit(token_ws)
    except TransbankError:
        return render(request, "error.html", {"message": "No fue posible confirmar el pago."})

    buy_order = respuesta.get("buy_order")
    if not buy_order:
        return render(request, "error.html", {"message": "La respuesta de pago no incluye una orden válida."})
    transaccion = get_object_or_404(Transaccion, buy_order=buy_order)
    try:
        monto_autorizado = Decimal(str(respuesta.get("amount"))).quantize(Decimal("0.01"))
    except (InvalidOperation, TypeError):
        monto_autorizado = None

    if respuesta.get("status") == "AUTHORIZED" and monto_autorizado == transaccion.costo_total:
        transaccion.pagado = True
        transaccion.save(update_fields=["pagado"])
        return render(
            request,
            "success.html",
            {
                "transaccion": transaccion,
                "modo_prueba": settings.TRANSBANK["INTEGRATION_TYPE"] == "TEST",
            },
        )

    return render(request, "error.html", {"message": "El pago no fue autorizado o el monto no coincide."})


@login_required
def transacciones_usuario(request):
    transacciones = Transaccion.objects.filter(propietario=request.user).order_by("-ID")
    return render(request, "transacciones_usuario.html", {"transacciones": transacciones})


@require_GET
def buscar_transaccion(request):
    codigo = request.GET.get("numero_seguimiento", "").strip()
    try:
        codigo = uuid.UUID(codigo)
    except (ValueError, TypeError, AttributeError):
        return JsonResponse({"error": "Ingresa un código de seguimiento válido."}, status=400)

    try:
        transaccion = Transaccion.objects.get(codigo_seguimiento=codigo)
    except Transaccion.DoesNotExist:
        return JsonResponse({"error": "No se encontró el envío."}, status=404)

    return JsonResponse(
        {
            "codigo_seguimiento": str(transaccion.codigo_seguimiento),
            "estado_envio": transaccion.get_estado_envio_display(),
            "tipo_paquete": transaccion.get_tipo_paquete_display(),
            "tipo_envio": transaccion.get_tipo_envio_display(),
        }
    )


@permission_required("principal.change_transaccion", raise_exception=True)
def currier_view(request):
    transacciones = Transaccion.objects.order_by("-ID")
    return render(request, "cargar_transaccion.html", {"transacciones": transacciones})
