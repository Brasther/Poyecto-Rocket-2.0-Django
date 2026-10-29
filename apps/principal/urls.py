from django.urls import path

from . import views


urlpatterns = [
    path("", views.cargarInicio, name="home"),
    path("acerca/", views.cargarQuienesSomos, name="quienes_somos"),
    path("powered-by/", views.cargarPoweredBy, name="powered_by"),
    path("terminos/", views.cargarTerminosYcondiciones, name="terminos"),
    path("registrarse/", views.signup, name="signup"),
    path("iniciar-sesion/", views.signin, name="signin"),
    path("cerrar-sesion/", views.signout, name="logout"),
    path("envios/nuevo/", views.formulario, name="formulario"),
    path("envios/crear/", views.iniciar_transaccion, name="iniciar_transaccion"),
    path("envios/mios/", views.transacciones_usuario, name="mis_transacciones"),
    path("envios/panel/", views.cargarTransaccion, name="cargarTransaccion"),
    path("envios/<int:transaccion_id>/editar/", views.editar_transaccion, name="editar_transaccion"),
    path("envios/<int:transaccion_id>/eliminar/", views.eliminar_transaccion, name="eliminar_transaccion"),
    path("envios/<int:transaccion_id>/estado/", views.editar_estado_envio, name="editar_estado_envio"),
    path("seguimiento/buscar/", views.buscar_transaccion, name="buscar_transaccion"),
    path("pagos/transbank/confirmar/", views.completar_transaccion, name="completar_transaccion"),
]
