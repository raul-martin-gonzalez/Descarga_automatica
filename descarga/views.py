from django.shortcuts import render
from django.http import HttpResponse 
import sys
import time
import os

# Create your views here.
def view_descarga (request):
    print('Hola aqui empieza todo')
    i = 3
    v = 4
    print(i+v)
    print('parece que funciona')
    print('ya estamos en internet')
    time.sleep(15)
    # Cierra el servidor Django
    shutdown_server()
    
    return HttpResponse('Hola mundo estoy aqui probando')

def shutdown_server():
    os._exit(0)