from django.urls import path
from . import views

from django.urls import path
#from .views import iniciar_transaccion, completar_transaccion

urlpatterns = [
    path('',views.cargarInicio, name='home'),
    path('quienesSomos',views.cargarQuienesSomos),
    path('poweredby',views.cargarPoweredBy),
    path('terminosYcon',views.cargarTerminosYcondiciones),
    
    path('registrarse',views.signup, name='signup'),
    path('iniciarSesion',views.signin, name='signin'),
    path('cerrarSesion', views.signout, name='logout'),
    path('formulario', views.formulario, name='formulario'),

    #path('transbank/iniciar-transaccion/', views.iniciar_transaccion_trans, name='iniciar_transaccion_trans'),
    path('transbank/completar-transaccion/', views.completar_transaccion, name='completar_transaccion'),
#django
    path('iniciar_transaccion/', views.iniciar_transaccion, name='iniciar_transaccion'),

    #path('agregarProductoForm', views.agregarProducto, name='formulario'),
    path('editar_transaccion/<int:transaccion_id>/', views.editar_transaccion, name='editar_transaccion'),
    path('cargarTransaccion', views.cargarTransaccion, name='cargarTransaccion'),
    path('eliminar_transaccion/<int:transaccion_id>/', views.eliminar_transaccion, name='eliminar_transaccion'),

    path('buscar-transaccion/', views.buscar_transaccion, name='buscar-transaccion'),

    path('mis-transacciones', views.transacciones_usuario, name='mis_transacciones'),

    path('cargar_transaccion', views.currier_view, name='currier_cargar_transaccion'),
    path('editar_estado_envio/<int:transaccion_id>/', views.editar_estado_envio, name='editar_estado_envio'),



]


'''
urlpatterns = [
    path('',views.cargarInicio, name='home'),
    path('quienesSomos', views.cargarQuienesSomos, name='quienesSomos'),
    path('poweredby', views.cargarPoweredBy, name='poweredby'),
    path('terminosYcon', views.cargarTerminosYcondiciones, name='terminosYcon'),
    path('registrarse', views.signup, name='signup'),
    path('iniciarSesion', views.signin, name='signin'),
    path('cerrarSesion', views.logout, name='logout'),
    path('formulario', views.formulario, name='formulario'),
    path('transbank/completar-transaccion/', views.completar_transaccion, name='completar_transaccion'),
    path('iniciar_transaccion/', views.iniciar_transaccion, name='iniciar_transaccion'),
    path('editar_transaccion/<int:transaccion_id>/', views.editar_transaccion, name='editar_transaccion'),
    path('cargarTransaccion', views.cargarTransaccion, name='cargarTransaccion'),
    path('eliminar_transaccion/<int:transaccion_id>/', views.eliminar_transaccion, name='eliminar_transaccion'),
    path('buscar-transaccion/', views.buscar_transaccion, name='buscar-transaccion'),
    path('mis-transacciones', views.transacciones_usuario, name='mis_transacciones'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    '''