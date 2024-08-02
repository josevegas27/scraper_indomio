import requests
import pytesseract 
from PIL import Image
import os
import time
from tools import *
pytesseract.pytesseract.tesseract_cmd = r".\Tesseract-OCR\tesseract.exe"


inmuebles_con_imagenes = 'inmuebles.csv'
archivo_final = 'data.csv'

try:
    time.sleep(3)
    convertir_a_texto(inmuebles_con_imagenes, archivo_final)
except:
    print("No se encuentra el archivo `inmuebles.csv` o ha ocurrido un error al intentar leerlo")




