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
server_url = 'http://localhost:8000/'  # URL de la página de inicio
while not is_server_running(server_url):
    print("Esperando a que el servidor inicie...")
    time.sleep(1)

print("El servidor está activo. Iniciando prueba de Selenium...")

# Inicializar el driver de Chrome
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # Abrir la página de inicio
    driver.get(server_url)

    time.sleep(5)

    # Localizar el campo de búsqueda del número de seguimiento
    search_input = driver.find_element('id', 'numero-seguimiento')  
    search_input.send_keys('292670')  

    # Enviar el formulario de búsqueda
    search_input.send_keys(Keys.RETURN)

    # Esperar unos segundos para que se procese la búsqueda
    time.sleep(5)

    assert "Detalles del pedido" in driver.page_source

    print("Prueba de búsqueda de pedido completada exitosamente.")

finally:
    # Cerrar el navegador al finalizar
    driver.quit()
    # Terminar el servidor Django
    server_process.terminate()
