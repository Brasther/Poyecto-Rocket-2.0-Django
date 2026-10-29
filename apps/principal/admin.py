from django.contrib import admin

from .models import Producto, Transaccion


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("sku", "nombre", "precio", "stock")
    search_fields = ("nombre",)


@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ("codigo_seguimiento", "propietario", "estado_envio", "pagado", "costo_total")
    list_filter = ("estado_envio", "pagado", "tipo_envio")
    search_fields = ("codigo_seguimiento", "buy_order")
    readonly_fields = ("codigo_seguimiento", "buy_order", "costo_total")
