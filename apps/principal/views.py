from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages #
from django.core import serializers #
from django.db import IntegrityError#
from django.http import HttpResponse,HttpResponseBadRequest #

import json

from .models import *
import os                   
from django.conf import settings
# Create your views here.
from django.shortcuts import render, redirect
from django.conf import settings
from transbank.webpay.webpay_plus.transaction import Transaction






def cargarInicio(request):
    return render(request,"inicio.html")



def cargarInicio(request):
    
    return render(request,"inicio.html")

def cargarQuienesSomos(request):
    
    return render(request,"quienesSomos.html")



def destinatario(request):
    
    return render(request,"destinatario.html")

def cargarPoweredBy(request):
    
    return render(request,"poweredby.html")

def cargarTerminosYcondiciones(request):
    
    return render(request,"terminosYcon.html")

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
  




#------------------------------------------------------------------------------------------#     

def iniciar_transaccion_trans(request):
    if request.method == 'POST':
        # Procesamiento de la transacción
        amount = request.POST.get('amount')
        costo_total = request.POST.get('costoTotal') # Obtener el costoTotal del formulario

        buy_order = 'ordenCompra12345678'
        session_id = 'sesion1234564'
        return_url = request.build_absolute_uri('/transbank/completar-transaccion/')

        response = Transaction().create(buy_order, session_id, amount, return_url)
        
        if 'token' in response and 'url' in response:
            return redirect(response['url'] + '?token_ws=' + response['token'])
        else:
            return render(request, 'error.html', {'message': 'Error al iniciar la transacción.'})
    


def completar_transaccion(request):
    token = request.GET.get('token_ws')
    response = Transaction().commit(token)
    
    
    if 'response_code' in response and response['response_code'] == 0:
        return render(request, 'success.html', {'response': response})
    else:
        # Manejo de errores
        return render(request, 'error.html', {'message': 'Error al completar la transacción.'})


#------------------------------------------------------------------------------------------#     

def formulario(request):
    transacciones = Transaccion.objects.all()
    return render(request, 'formulario.html', {'transacciones': transacciones})

def cargarTransaccion(request):
    transacciones = Transaccion.objects.all()
    return render(request,"cargar_transaccion.html", {'transacciones': transacciones})


from .forms import TransaccionForm

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
            print(form.errors)  # Imprimir errores en la consola del servidor
    else:
        form = TransaccionForm(instance=transaccion)
    return render(request, 'editar_transaccion.html', {'form': form, 'transaccion': transaccion})

    #return render(request, 'editar_transaccion.html', {'form': form, 'transaccion': transaccion})

def eliminar_transaccion(request, transaccion_id):
    transaccion = get_object_or_404(Transaccion, ID=transaccion_id)
    transaccion.delete()
    messages.success(request, 'Transacción eliminada correctamente.')
    return redirect('cargarTransaccion')


from decimal import Decimal
import random

def generar_ID():
    while True:
        ID = ''.join(random.choices('0123456789', k=6))
        if not Transaccion.objects.filter(ID=ID).exists():
            return ID


def iniciar_transaccion(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre_remitente = request.POST['nombreRemitente']
        rut_remitente = request.POST['rutRemitente']
        direccion_remitente = request.POST['direccionRemitente']
        email_remitente = request.POST.get('Email', '')
        telefono_remitente = request.POST.get('telefonoRemitente', '')

        # Obtener datos del destinatario
        nombre_destinatario = request.POST['nombreDestinatario']
        rut_destinatario = request.POST['rutDestinatario']
        direccion_destinatario = request.POST['direccionDestinatario']
        email_destinatario = request.POST.get('emailDestinatario', '')
        telefono_destinatario = request.POST.get('telefonoDestinatario', '')

        # Obtener datos del envío
        tipo_paquete = request.POST['tipoPaquete']
        tipo_envio = request.POST['tipoEnvio']
        pagado = 'pagado' in request.POST
        por_pagar = 'porPagar' in request.POST
        costo_total = request.POST.get('totalAmount', '0.0')
        if costo_total == '':
            costo_total = '0.0'
        costo_total = Decimal(costo_total)


        ID = generar_ID()

        # Crear la transacción en la base de datos

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
            costo_total=costo_total
        )

        

        # Guardar la instancia de Transaccion
        transaccion.save()

        # Iniciar la transacción con Transbank
        amount = str(costo_total)
        buy_order = 'ordenCompra12345678'
        session_id = 'sesion1234564'
        return_url = request.build_absolute_uri('/transbank/completar-transaccion/')

        response = Transaction().create( buy_order, session_id, amount, return_url)

        if 'token' in response and 'url' in response:
            return redirect(response['url'] + '?token_ws=' + response['token'])
        else:
            return render(request, 'error.html', {'message': 'Error al iniciar la transacción.'})

    # Obtener todas las transacciones
    transacciones = Transaccion.objects.all()
    return render(request, 'formulario.html', {'transacciones': transacciones})

#------------------------------------------------------------------------------------------#

'''
def agregarProducto(request):
    if request.method == 'POST':
        v_nombre = request.POST['txtNombre']
        v_stock = request.POST['txtStock']
        v_precio = request.POST['txtPrecio']
        v_descripcion = request.POST['txtDescripcion']
        v_nota = request.POST['txtNota']  # Nuevo campo

        # Verificar si el SKU ya existe
        while True:
            v_sku = generar_ID()
            if not Producto.objects.filter(sku=v_sku).exists():
                break

        try:
            Producto.objects.create(
                sku=v_sku,
                nombre=v_nombre,
                stock=v_stock,
                precio=v_precio,
                descripcion=v_descripcion,
                nota=v_nota,  # Nuevo campo
            )
        except IntegrityError:
            messages.error(request, 'El SKU ya existe. Por favor, elija otro SKU.')
            return redirect('formulario')

        return redirect('formulario')

    # Obtener todos los productos para pasarlos al contexto
    productos = Producto.objects.all()
    return render(request, 'formulario.html', {'prod': productos})
    '''
