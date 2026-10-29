from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError#

from django.http import JsonResponse, HttpResponseBadRequest
from decimal import Decimal
from .models import Transaccion
from .forms import TransaccionForm
from transbank.common.integration_api_keys import IntegrationApiKeys
from transbank.common.integration_commerce_codes import IntegrationCommerceCodes
from transbank.common.integration_type import IntegrationType
from transbank.common.options import WebpayOptions
from transbank.webpay.webpay_plus.transaction import Transaction
import random


def obtener_transaccion_transbank():
    configuracion = settings.TRANSBANK
    entorno = configuracion['INTEGRATION_TYPE']
    if entorno not in {'TEST', 'LIVE'}:
        raise ImproperlyConfigured('TRANSBANK_INTEGRATION_TYPE debe ser TEST o LIVE.')

    if entorno == 'TEST':
        codigo_comercio = configuracion['COMMERCE_CODE'] or IntegrationCommerceCodes.WEBPAY_PLUS
        api_key = configuracion['API_KEY'] or IntegrationApiKeys.WEBPAY
    else:
        codigo_comercio = configuracion['COMMERCE_CODE']
        api_key = configuracion['API_KEY']
        if not codigo_comercio or not api_key:
            raise ImproperlyConfigured(
                'Define TRANSBANK_COMMERCE_CODE y TRANSBANK_API_KEY para usar el entorno LIVE.'
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
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save() #guarda el user en la base
                login(request, user) #cookies
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "Usuario Ya existente."})
        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Las Contraseñas no coninciden."})

def home(request):
    return render(request, 'home.html')


@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "Usuario o Contraseña incorrecto."})
        login(request, user)
        return redirect('home')




from django import forms

class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = '__all__'

    def clean_email_destinatario(self):
        email_destinatario = self.cleaned_data.get('email_destinatario')
        if email_destinatario and '@' not in email_destinatario:
            raise forms.ValidationError("Ingrese un email válido.")
        return email_destinatario
#------------------------------------------------------------------------------------------------------------------------------------------
def home(request):
    return render(request, 'home.html')


def formulario(request):
    transacciones = Transaccion.objects.all()
    return render(request, 'formulario.html', {'transacciones': transacciones})


def cargarTransaccion(request):
    transacciones = Transaccion.objects.all()
    return render(request, "cargar_transaccion.html", {'transacciones': transacciones})

from django.http import HttpResponse
def editar_estado_envio(request, transaccion_id):
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado_envio')
        transaccion = Transaccion.objects.get(ID=transaccion_id)
        transaccion.estado_envio = nuevo_estado
        transaccion.save()
        return redirect('cargarTransaccion') 
    else:
        return HttpResponse("Método no permitido")


@login_required
def editar_transaccion(request, transaccion_id):
    transaccion = get_object_or_404(Transaccion, ID=transaccion_id)
    if request.method == 'POST':
        form = TransaccionForm(request.POST, instance=transaccion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transacción modificada correctamente.')
            return redirect('cargarTransaccion')  
        else:
            messages.error(request, 'Hubo un error al procesar el formulario.')
            print(form.errors)
    else:
        form = TransaccionForm(instance=transaccion)
    return render(request, 'editar_transaccion.html', {'form': form, 'transaccion': transaccion})

@login_required
def eliminar_transaccion(request, transaccion_id):
    transaccion = get_object_or_404(Transaccion, ID=transaccion_id)
    transaccion.delete()
    messages.success(request, 'Transacción eliminada correctamente.')
    return redirect('cargarTransaccion')


def generar_ID():
    while True:
        ID = ''.join(random.choices('0123456789', k=6))
        if not Transaccion.objects.filter(ID=ID).exists():
            return ID

@login_required
def iniciar_transaccion(request):
    if request.method == 'POST':
        nombre_remitente = request.POST.get('nombreRemitente')
        rut_remitente = request.POST.get('rutRemitente')
        direccion_remitente = request.POST.get('direccionRemitente')
        email_remitente = request.POST.get('Email', '')
        telefono_remitente = request.POST.get('telefonoRemitente', '')

        nombre_destinatario = request.POST.get('nombreDestinatario')
        rut_destinatario = request.POST.get('rutDestinatario')
        direccion_destinatario = request.POST.get('direccionDestinatario')
        email_destinatario = request.POST.get('emailDestinatario', '')
        telefono_destinatario = request.POST.get('telefonoDestinatario', '')

        tipo_paquete = request.POST.get('tipoPaquete')
        tipo_envio = request.POST.get('tipoEnvio')
        pagado = 'pagado' in request.POST
        por_pagar = 'porPagar' in request.POST
        costo_total = request.POST.get('totalAmount', '0.0')
        if costo_total == '':
            costo_total = '0.0'
        costo_total = Decimal(costo_total)

        session_id = request.user.username
        buy_order = f'ordenCompra-{session_id}{Transaccion.objects.count()}'

        ID = generar_ID()

        transaccion = Transaccion.objects.create(
            ID=ID,
            nombre_remitente=nombre_remitente,
            rut_remitente=rut_remitente,
            direccion_remitente=direccion_remitente,
            email_remitente=email_remitente,
            telefono_remitente=telefono_remitente,
            nombre_destinatario=nombre_destinatario,
            rut_destinatario=rut_destinatario,
            direccion_destinatario=direccion_destinatario,
            email_destinatario=email_destinatario,
            telefono_destinatario=telefono_destinatario,
            tipo_paquete=tipo_paquete,
            tipo_envio=tipo_envio,
            pagado=pagado,
            por_pagar=por_pagar,
            costo_total=costo_total,
            session_id=session_id,
            buy_order=buy_order
        )

        transaccion.save()

        amount = str(costo_total)
        return_url = request.build_absolute_uri('/transbank/completar-transaccion/')
        response = obtener_transaccion_transbank().create(buy_order, session_id, amount, return_url)

        if 'token' in response and 'url' in response:
            return redirect(response['url'] + '?token_ws=' + response['token'])
        else:
            return render(request, 'error.html', {'message': 'Error al iniciar la transacción.'})

    transacciones = Transaccion.objects.all()
    return render(request, 'formulario.html', {'transacciones': transacciones})


def transacciones_usuario(request):
    username = request.user.username
    transacciones = Transaccion.objects.filter(session_id=username)
    return render(request, 'transacciones_usuario.html', {'transacciones': transacciones})



def buscar_transaccion(request):
    numero_seguimiento = request.GET.get('numero_seguimiento')
    if numero_seguimiento:
        try:
            transaccion = Transaccion.objects.get(ID=numero_seguimiento)
            datos = {
                'ID': transaccion.ID,
                'nombre_remitente': transaccion.nombre_remitente,
                'direccion_remitente': transaccion.direccion_remitente,
                'nombre_destinatario': transaccion.nombre_destinatario,
                'direccion_destinatario': transaccion.direccion_destinatario,
                'tipo_paquete': transaccion.get_tipo_paquete_display(),
                'tipo_envio': transaccion.get_tipo_envio_display(),
                'pagado': transaccion.pagado,
                'por_pagar': transaccion.por_pagar,
                'costo_total': float(transaccion.costo_total),  # Convertir a float si es decimal
            }
            return JsonResponse(datos)
        except Transaccion.DoesNotExist:
            return JsonResponse({'error': 'No se encontró la transacción.'}, status=404)
    return JsonResponse({'error': 'Número de seguimiento no proporcionado.'}, status=400)











#-------------
@login_required
def completar_transaccion(request):
    token_ws = request.GET.get('token_ws')
    if not token_ws:
        return render(request, 'error.html', {'message': 'No se recibió el token_ws.'})

    response = obtener_transaccion_transbank().commit(token_ws)
    if response['status'] == 'AUTHORIZED':
        transaccion = Transaccion.objects.get(buy_order=response['buy_order'])
        transaccion.pagado = True
        transaccion.save()

        return render(request, 'success.html', {'response': response, 'transaccion': transaccion})
    else:
        return render(request, 'error.html', {'message': 'La transacción no fue autorizada.'})
    




@login_required
def currier_view(request):
    if request.user.username != 'Currier':
        return redirect('home')
    
    transacciones = Transaccion.objects.all()  # Obtiene todas las transacciones
    return render(request, 'cargar_transaccion.html', {'transacciones': transacciones, 'read_only': True})
