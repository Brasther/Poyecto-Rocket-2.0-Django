from django.shortcuts import render
from django.views import View           #
from django.http import JsonResponse    #
from apps.principal.models import Producto #

# Create your views here.

class ObtenerProducto(View):
    def get(self, request):
        producto = Producto.objects.all()
        return JsonResponse(list(producto.values()),safe=False)
