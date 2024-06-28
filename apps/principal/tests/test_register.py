import subprocess
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Ruta completa al archivo manage.py
manage_py_path = r'C:\Users\sebas\OneDrive\Escritorio\Poyecto_Rocket_2.0_Django\manage.py'

# Función para verificar si el servidor está activo
def is_server_running(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.ConnectionError:
        return False

# Iniciar el servidor Django
server_process = subprocess.Popen(['python', manage_py_path, 'runserver'])

# Esperar a que el servidor esté activo
server_url = 'http://localhost:8000/registrarse'  # Ajusta esta URL según tu configuración
while not is_server_running(server_url):
    print("Esperando a que el servidor inicie...")
    time.sleep(1)

print("El servidor está activo. Iniciando prueba de Selenium...")

try:
    # Inicializar el driver de Chrome
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Abrir la página de registro
    driver.get(server_url)

    # Simular el proceso de registro
    username_input = driver.find_element('name', 'username')
    username_input.send_keys('testuser1')

    password_input = driver.find_element('name', 'password1')
    password_input.send_keys('testpassword1')

    password_confirm_input = driver.find_element('name', 'password2')
    password_confirm_input.send_keys('testpassword1')

    # Enviar el formulario de registro
    password_confirm_input.send_keys(Keys.RETURN)

    time.sleep(2)

    # Verificar que el usuario ha sido registrado exitosamente
    assert "Registro completo" in driver.page_source

    print("Prueba de registro completada exitosamente.")

finally:
    # Cerrar el navegador al finalizar
    if 'driver' in locals():
        driver.quit()

    # Terminar el servidor Django
    if 'server_process' in locals():
        server_process.terminate()
