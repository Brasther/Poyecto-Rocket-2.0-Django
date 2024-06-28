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
server_url = 'http://localhost:8000/iniciarSesion'  # Ajusta esta URL según tu configuración de login
while not is_server_running(server_url):
    print("Esperando a que el servidor inicie...")
    time.sleep(1)

print("El servidor está activo. Iniciando prueba de Selenium para el inicio de sesión...")

try:
    # Inicializar el driver de Chrome
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Abrir la página de inicio de sesión
    driver.get(server_url)

    # Simular el proceso de inicio de sesión
    username_input = driver.find_element('name', 'username')
    username_input.send_keys('testuser1')  

    password_input = driver.find_element('name', 'password')
    password_input.send_keys('testpassword1') 

    # Enviar el formulario de inicio de sesión
    password_input.send_keys(Keys.RETURN)

    time.sleep(2)

    assert "Bienvenido" in driver.page_source  

    print("Prueba de inicio de sesión completada exitosamente.")

finally:
    # Cerrar el navegador al finalizar
    if 'driver' in locals():
        driver.quit()

    # Terminar el servidor Django
    if 'server_process' in locals():
        server_process.terminate()
