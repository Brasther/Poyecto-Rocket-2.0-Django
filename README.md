# Rocket Tracking

Prototipo web en Django para gestionar envíos y consultar su seguimiento. El proyecto permite registrar remitentes y destinatarios, elegir tamaño y modalidad de envío, iniciar un pago de prueba con Webpay Plus y actualizar el estado de una entrega.

## Funciones

- Registro e inicio de sesión de usuarios.
- Formulario de envío con datos de remitente, destinatario, tamaño y tipo de entrega.
- Inicio y confirmación de pagos mediante el SDK de Transbank.
- Consulta de seguimiento usando el identificador de la transacción.
- Vistas para consultar transacciones y actualizar el estado del envío.
- Interfaz en español construida con plantillas Django, CSS y JavaScript.

## Tecnologías

- Python 3.12 o superior
- Django 5.2
- SQLite para desarrollo local
- SDK oficial de Transbank para Python
- HTML, CSS, JavaScript y Bootstrap

## Ejecutar localmente

En PowerShell, desde la raíz del repositorio:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:DJANGO_SECRET_KEY = "clave-local-solo-para-desarrollo"
$env:DJANGO_DEBUG = "true"
$env:DJANGO_ALLOWED_HOSTS = "127.0.0.1,localhost"
$env:TRANSBANK_INTEGRATION_TYPE = "TEST"
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe manage.py runserver
```

Luego abre <http://127.0.0.1:8000/>. La aplicación usa SQLite local; las migraciones crean una base de datos nueva al iniciar. El SDK se configura en modo de integración de prueba por defecto. Para una integración real se deben configurar `TRANSBANK_COMMERCE_CODE` y `TRANSBANK_API_KEY` como variables de entorno y revisar la documentación oficial de Transbank.

## Configuración

| Variable | Uso | Valor local predeterminado |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | Clave de Django | Obligatoria; define una clave local propia |
| `DJANGO_DEBUG` | Modo de depuración | `false` |
| `DJANGO_ALLOWED_HOSTS` | Hosts separados por coma | `localhost,127.0.0.1` |
| `TRANSBANK_INTEGRATION_TYPE` | Entorno de Webpay | `TEST` |
| `TRANSBANK_COMMERCE_CODE` | Código del comercio | Código de integración de prueba |
| `TRANSBANK_API_KEY` | Llave API | Llave de integración de prueba |

No guardes claves reales ni bases de datos locales en Git.

## Estado y seguridad

Este repositorio corresponde a un prototipo académico. No está listo para producción: maneja datos personales de remitentes y destinatarios, y aún requiere una revisión de permisos por vista, privacidad del seguimiento, validación de pagos, despliegue seguro y protección de datos. Usa únicamente datos ficticios al ejecutarlo o mostrarlo.

Los valores de integración de prueba de Transbank son públicos y sirven para desarrollo; no son credenciales de producción. Django se inicia sin `DEBUG` y requiere `DJANGO_SECRET_KEY` explícita. No reutilices la clave del ejemplo fuera de una máquina local.

## Estructura

```text
tracking/             Configuración del proyecto Django
apps/principal/       Aplicación de envíos, vistas, modelos y plantillas
apps/principal/static/ CSS, JavaScript e imágenes de la interfaz
imagenesProducto/    Imágenes utilizadas por el proyecto
```
