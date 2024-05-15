from django.urls import path
from . import views


from django.urls import path
from .views import iniciar_transaccion, completar_transaccion

urlpatterns = [
    path('',views.cargarInicio, name='home'),
    path('clima',views.cargarClima),
    path('quienesSomos',views.cargarQuienesSomos),

    path('registrarse',views.signup, name='signup'),
    path('iniciarSesion',views.signin, name='signin'),
    path('cerrarSesion',views.signout, name='logout'),
    path('formulario',views.formulario),
    path('transbank/iniciar-transaccion/', iniciar_transaccion, name='iniciar_transaccion'),
    path('transbank/completar-transaccion/', completar_transaccion, name='completar_transaccion'),



]