import requests
import pytesseract 
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"



def descargar_imagen(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open('./imagenes_telefonos/'+filename,'wb') as file:
            file.write(response.content)


archivo_csv = open('venta_la_coruna.csv','r', encoding='utf-8')
archivo_final = open('datos_finales.csv','w')

head = archivo_csv.readline()
archivo_final.write(head)
for i,lines in enumerate(archivo_csv.readlines()):
    print(lines)
    campos = lines.split(',')
    url = campos[8]
    print(campos)

    if url != '':
        
        name = f'imagen{i}.jpg'

        descargar_imagen(url, name)

        img = Image.open(f'./imagenes_telefonos/imagen{i}.jpg')
        texto = pytesseract.image_to_string(img)

    else:
        texto = ' '
    

    campos[8] = texto.strip()
    linea = ','.join(campos)
    print('??????????????', linea)
    archivo_final.write(linea)


archivo_final.close()
archivo_csv.close()