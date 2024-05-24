from django.urls import path
from . import views

from django.urls import path
from .views import iniciar_transaccion, completar_transaccion

urlpatterns = [
    path('',views.cargarInicio, name='home'),
    path('quienesSomos',views.cargarQuienesSomos),
    path('poweredby',views.cargarPoweredBy),
    path('terminosYcon',views.cargarTerminosYcondiciones),
    
    path('registrarse',views.signup, name='signup'),
    path('iniciarSesion',views.signin, name='signin'),
    path('cerrarSesion',views.signout, name='logout'),
    path('formulario', views.formulario, name='formulario'),
    path('destinatario', views.destinatario, name='destinatario'),

    path('transbank/iniciar-transaccion/', views.iniciar_transaccion_trans, name='iniciar_transaccion_trans'),
    path('transbank/completar-transaccion/', views.completar_transaccion, name='completar_transaccion'),

#django
    path('iniciar_transaccion/', views.iniciar_transaccion, name='iniciar_transaccion'),

    #path('agregarProductoForm', views.agregarProducto, name='formulario'),
    path('editar_transaccion/<int:transaccion_id>/', views.editar_transaccion, name='editar_transaccion'),
    path('cargarTransaccion/', views.cargarTransaccion, name='cargarTransaccion'),
    path('eliminar_transaccion/<int:transaccion_id>/', views.eliminar_transaccion, name='eliminar_transaccion'),

    path('buscar-transaccion/', views.buscar_transaccion, name='buscar-transaccion'),




]