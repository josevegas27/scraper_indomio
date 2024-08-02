import requests
import pytesseract 
from PIL import Image
import os
import time
from tools import *
pytesseract.pytesseract.tesseract_cmd = r".\Tesseract-OCR\tesseract.exe"


inmuebles_con_imagenes = 'inmuebles.csv'
archivo_final = 'data.csv'

star_time = time.time()
os.system(f'scrapy crawl indomio -o {inmuebles_con_imagenes}')
finish_time = time.time()
print('\nTime:', finish_time - star_time)


time.sleep(3)
convertir_a_texto(inmuebles_con_imagenes, archivo_final)


