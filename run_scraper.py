import requests
import pytesseract 
from PIL import Image
import os
import time
from tools import *

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


print(os.getcwd())

star_time = time.time()
# os.system('scrapy crawl venta -o ventas_inmueble.csv')
finish_time = time.time()
print('\nTime:', finish_time - star_time)

star_time = time.time()
# os.system('scrapy crawl alquiler -o alquiler_inmueble.csv')
finish_time = time.time()
print('\nTime:', finish_time - star_time)


archivo_temp = 'data_temp.csv'
archivo_final = 'data.csv'

# time.sleep(3)
# combinar_archivos('ventas_inmueble.csv', 'alquiler_inmueble.csv', archivo_temp)

# time.sleep(3)
convertir_a_texto(archivo_temp, archivo_final)

time.sleep(3)
# del archivo_temp

