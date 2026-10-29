# Rocket Tracking

Prototipo académico en Django para crear envíos, consultar su estado y explorar un flujo de pago con Transbank. No representa una empresa real ni crea órdenes de transporte comerciales.

## Funcionalidades

- Registro, inicio y cierre de sesión con formularios de autenticación de Django.
- Creación de envíos con validación en servidor y cálculo de precio que no depende del valor enviado por el navegador.
- Códigos de seguimiento UUID difíciles de adivinar; la consulta pública muestra solo estado y tipo de servicio, sin nombres ni direcciones.
- Vista de “Mis envíos” limitada a la cuenta autenticada.
- Panel de gestión protegido por permisos de Django para consultar envíos y cambiar su estado.
- Flujo Webpay Plus en entorno de integración `TEST` por defecto.

## Tecnologías

- Python 3.12 o superior
- Django 5.2
- SQLite local
- SDK oficial `transbank-sdk` 6.1
- Bootstrap 5.3 y JavaScript

## Instalación local

En PowerShell, desde la carpeta del repositorio:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:DJANGO_SECRET_KEY = & .\.venv\Scripts\python.exe -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
$env:DJANGO_DEBUG = "true"
$env:DJANGO_ALLOWED_HOSTS = "127.0.0.1,localhost"
$env:TRANSBANK_INTEGRATION_TYPE = "TEST"
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe manage.py createsuperuser
.venv\Scripts\python.exe manage.py runserver
```

Abre <http://127.0.0.1:8000/>. La primera migración crea una base SQLite vacía en `db.sqlite3`; ese archivo está ignorado por Git. No hay cuentas, envíos ni datos de ejemplo precargados.

La cuenta creada con `createsuperuser` puede abrir el panel y administrar envíos. Para habilitar a otra persona, crea su cuenta en el sitio de administración y asígnale los permisos `view_transaccion` y `change_transaccion`.

## Variables de entorno

| Variable | Uso | Valor predeterminado |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | Clave de firma de Django | Obligatoria |
| `DJANGO_DEBUG` | Activa depuración local | `false` |
| `DJANGO_ALLOWED_HOSTS` | Hosts separados por coma | `localhost,127.0.0.1` |
| `TRANSBANK_INTEGRATION_TYPE` | Entorno Webpay | `TEST` |
| `TRANSBANK_COMMERCE_CODE` | Código de comercio | Credencial pública de integración de prueba |
| `TRANSBANK_API_KEY` | Llave API | Credencial pública de integración de prueba |

Los valores de prueba de Transbank se usan solo cuando el entorno es `TEST`. El entorno `LIVE` requiere configurar explícitamente las credenciales comerciales. No guardes claves reales ni archivos `.env` en Git.

## Datos y seguridad

La base de datos no se distribuye. Cada persona crea su propia base local con `migrate`. Usa únicamente información ficticia: el modelo de envío incluye RUT, direcciones, teléfonos y correos.

Este proyecto es un ejemplo de aprendizaje, no está preparado para producción. Antes de desplegarlo con datos reales hacen falta, entre otras cosas, una revisión completa de privacidad y permisos, límites contra abuso, HTTPS, configuración segura de cookies y una evaluación independiente del flujo de pagos.

## Licencia

Rocket Tracking se distribuye bajo la licencia [MIT](LICENSE). Puedes usar, modificar y redistribuir el proyecto, incluso comercialmente, siempre que conserves el aviso de copyright y el archivo de licencia en las copias o partes sustanciales del software.
