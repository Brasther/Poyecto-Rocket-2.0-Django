from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages #
from django.core import serializers #
from django.db import IntegrityError#
from django.http import HttpResponse #

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


def cargarClima(request):
    return render(request,"clima.html")


def cargarInicio(request):
    
    return render(request,"inicio.html")

def cargarQuienesSomos(request):
    
    return render(request,"quienesSomos.html")

def formulario(request):
    
    return render(request,"formulario.html")


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
def iniciar_transaccion(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        buy_order = 'ordenCompra12345678'
        session_id = 'sesion1234564'
        return_url = request.build_absolute_uri('/transbank/completar-transaccion/')

        response = Transaction().create(buy_order, session_id, amount, return_url)
        
        if 'token' in response and 'url' in response:
            return redirect(response['url'] + '?token_ws=' + response['token'])
        else:
            return render(request, 'error.html', {'message': 'Error al iniciar la transacción.'})
    else:
        return redirect('mostrar_formulario')

def completar_transaccion(request):
    token = request.GET.get('token_ws')
    response = Transaction().commit(token)
    
    if 'response_code' in response and response['response_code'] == 0:
        return render(request, 'success.html', {'response': response})
    else:
        return render(request, 'error.html', {'message': 'Error al completar la transacción.'})