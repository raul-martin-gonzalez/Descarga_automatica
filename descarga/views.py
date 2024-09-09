from django.shortcuts import render
from django.http import HttpResponse 
import time
from datetime import datetime, timedelta
import pandas as pd
import mysql.connector
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from google.cloud import storage
import sys
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# Create your views here.
@csrf_exempt
@require_http_methods(["POST"])
def view_descarga (request):
    print('Hola aqui empieza todo')
    i = 3
    v = 4
    print(i+v)
    print('parece que funciona')
    print('ya estamos ens internet')
    download_adn_upload()
    
    print('funcion terminada')
    time.sleep(10)
    # Cierra el servidor Django
    shutdown_server()
    
    return HttpResponse('Hola mundo estoy aqui probando')

def shutdown_server():
    os._exit(0)
    
    
def download_adn_upload():
    # Configuración de las opciones de Chrome para descargar 
    chrome_options = Options()
    directorio = "/tmp" # Directorio temporal para Cloud Run


    # Configura el directorio de descarga y desactiva la solicitud de ubicación de guardado
    prefs = {
        "download.default_directory": directorio,  # Establece la ubicación de descarga
        "download.prompt_for_download": False,  # Desactiva el cuadro de diálogo de descarga
        "download.directory_upgrade": True,  # Actualiza la ubicación de descarga
        "safebrowsing.enabled": True,  # Desactiva la verificación de sitios peligrosos para que no bloquee la descarga
        "download.suggested_filename": "precio_luz.csv"  # Sugiere un nombre para el archivo
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # configura y lanza e lnavegador Chrome
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    url = 'https://www.esios.ree.es/es/pvpc'
    driver.get(url)
    time.sleep(15)


    try:
        cookies = driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinDeclineAll")
        cookies.click()
    except Exception as e:
        print(f'Error al encontrar el botón de cookies: {e}')
        pass #continua la ejecucion incluso si ocurre un error

    pagina_datos = driver.find_element(By.XPATH, "//a[@class='esios-toolbar__buttons toolbar-analysis' and @target='_blank']")
    pagina_datos.click()

    time.sleep(10)

    # Obtén los identificadores de todas las ventanas
    windows = driver.window_handles
    # Cambia a la nueva ventana (la última ventana en la lista de identificadores)
    driver.switch_to.window(windows[-1])

    try:
        # Obtener la fecha de hoy
        hoy = datetime.now().date()
        # Restar un día para obtener la fecha de ayer
        ayer = hoy - timedelta(days=1)
        # Formatear la fecha de ayer en DD/MM/YYYY
        ayer_formateado = ayer.strftime("%d / %m / %Y")
        print(ayer_formateado, type(ayer_formateado))
        driver.execute_script("window.scrollBy(0, 500);") # Desplazamiento scroll
        inicio = driver.find_element(By.ID, "start-date")
        time.sleep(5)
        inicio.clear()
        time.sleep(5)
        inicio.send_keys(ayer_formateado + Keys.RETURN)
        time.sleep(5)
        driver.execute_script("window.scrollBy(0, 700);") # Desplazamiento scroll
        time.sleep(20)
        boton_exportacion = driver.find_element(By.ID, "export_multiple")
        boton_exportacion.click()
        # Esperar a que el menú desplegable esté visible
        wait = WebDriverWait(driver, 20)
        options_select = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'options_select')))

        # Encontrar y hacer clic en la primera opción (CSV)
        # Encuentra el primer div dentro de 'options_select'
        csv_option = options_select.find_element(By.XPATH, './div[@class="opt-ancle"]')
        print(csv_option.text)
        
        actions = ActionChains(driver)
        actions.move_to_element(csv_option).perform()
        time.sleep(15)
        # Hacer clic en el elemento después del hover
        csv_option.click()
        time.sleep(25)
        
    except Exception as e:
        print(f'Error al interactuar con la página de datos o exportación: {e}')
        pass #continua la ejecucion incluso si ocurre un error

    driver.close()
    
    def obtener_archivo_mas_reciente(directorio):
        # Listar todos los archivos en el directorio
        archivos = os.listdir(directorio)
        # Filtrar archivos que tengan la extensión .csv
        archivos_csv = [archivo for archivo in archivos if archivo.endswith('.csv')]
        # Si no hay archivos .csv, lanzar una excepción o manejar el caso
        if not archivos_csv:
            raise FileNotFoundError("No se encontraron archivos .csv en el directorio.")
        # Obtener las rutas completas de los archivos .csv
        rutas_archivos = [os.path.join(directorio, archivo) for archivo in archivos_csv]
        # Encontrar el archivo .csv más reciente basado en la fecha de modificación.
        archivo_reciente = max(rutas_archivos, key=os.path.getmtime)
        # Imprimir la ruta del archivo más reciente (para depuración)
        print(f"Archivo CSV más reciente: {archivo_reciente}")
        return os.path.basename(archivo_reciente)

    # Espera para asegurarse de que la descarga se complete
    time.sleep(25)

    # Obtén el archivo más reciente
    nombre_archivo_descargado = obtener_archivo_mas_reciente(directorio)
    print(f"Archivo descargado: {nombre_archivo_descargado}")

    # Fecha actual
    fecha_actual = datetime.now().strftime('%Y-%m-%d') #Formato: YYYY-MM-DD

    # Nuevo nombre para el archivo
    nombre_final = f'Precio_luz_{fecha_actual}.csv'

    # Ruta completa al archivo descargado
    ruta_descargado = os.path.join(directorio, nombre_archivo_descargado)

    # Ruta completa al archivo renombrado
    ruta_final = os.path.join(directorio, nombre_final)

    # Renombrar el archivo
    os.rename(ruta_descargado, ruta_final)
    print(f'Archivo renombrado a {nombre_final}')
    
    # ruta_credenciales = r'C:\Users\raulm\AppData\Roaming\gcloud\application_default_credentials.json'

    # Subir el archivo descargado a Google Cloud Storage
    def upload_to_gcs (bucket_name, source_file_name, destination_blob_name):
        print(f"Verificando el archivo: {source_file_name}") # Depuración
        
        # Verifica si la ruta es un archivo
        if not os.path.isfile(source_file_name):
            print(source_file_name)
            print(f"Contenido del directorio /tmp: {os.listdir('/tmp')}")  # Depuración adicional
            raise ValueError(f"{source_file_name} no es un archivo válido o no existe.")
            
        storage_client = storage.Client(project='practica-django')
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        
        print(f'Archivo {nombre_final} subido a {destination_blob_name}.')
        # Sube el archivo usando el objeto de archivo.
    bucket_name = 'descarga_automatizacion'
    
    downloaded_file = max([os.path.join(directorio, f) for f in os.listdir(directorio)], key=os.path.getctime)
    
    # nombre_archivo_local = os.path.join(directorio, nombre_final)
    nombre_archivo_gcs = f'datos_precio_luz/{nombre_final}'

    upload_to_gcs(bucket_name, downloaded_file, nombre_archivo_gcs)