from django.shortcuts import render
from django.http import HttpResponse 
import time
from datetime import datetime
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

# Create your views here.
def view_descarga (request):
    print('Hola aqui empieza todo')
    i = 3
    v = 4
    print(i+v)
    print('parece que funciona')
    print('ya estamos ens internet')
    download_adn_upload()
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
    time.sleep(10)


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
        driver.execute_script("window.scrollBy(0, 1200);") # Desplazamiento scroll
        time.sleep(5)
        boton_exportacion = driver.find_element(By.ID, "export_multiple")
        boton_exportacion.click()
        # Esperar a que el menú desplegable esté visible
        wait = WebDriverWait(driver, 10)
        options_select = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'options_select')))

        # Encontrar y hacer clic en la primera opción (CSV)
        # Encuentra el primer div dentro de 'options_select'
        csv_option = options_select.find_element(By.XPATH, './div[@class="opt-ancle"]')
        print(csv_option.text)
        
        actions = ActionChains(driver)
        actions.move_to_element(csv_option).perform()
        time.sleep(5)
        # Hacer clic en el elemento después del hover
        csv_option.click()
        time.sleep(10)
        
    except Exception as e:
        print(f'Error al interactuar con la página de datos o exportación: {e}')
        pass #continua la ejecucion incluso si ocurre un error

    driver.close()