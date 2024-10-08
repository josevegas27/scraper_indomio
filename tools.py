import requests
import pytesseract 
import time
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r".\Tesseract-OCR\tesseract.exe"

def combinar_archivos(csv1,csv2,csv3):
    a1, a2 = open(csv1, 'r', encoding='utf-8'), open(csv2, 'r', encoding='utf-8')
    a2.readline()
    
    with open(csv3,'w')  as b:
        b.write(a1.read())
        b.write(a2.read())

    a1.close()
    a2.close()


def descargar_imagen(url, filename, wait=None):
    response = requests.get(url, timeout=wait)
    if response.status_code == 200:
        with open('./imagenes_telefonos/'+filename,'wb') as file:
            file.write(response.content)
        return True
    return False


def convertir_a_texto(csv1, csv2):
    '''
    Convierte las imagenes del campo telefono del csv1 a texto y los sustituye en un archivo csv2
    '''
    num_peticiones = 0

    archivo_csv = open(csv1,'r', encoding='utf-8')
    archivo_final = open(csv2,'w')

    head = archivo_csv.readline()
    archivo_final.write(head)

    for i,lines in enumerate(archivo_csv.readlines()):
        campos = lines.split(',')
        url = campos[8]

        # if i < 0:
            # continue

        if url != '':
            
            print('conseguimos una url', i, '-----', url)
            num_peticiones += 1
            if num_peticiones == 70:
                time.sleep(5)
                num_peticiones = 0

            name = f'imagen{i}.jpg'
            if descargar_imagen(url, name):

                img = Image.open(f'./imagenes_telefonos/imagen{i}.jpg')
                texto = pytesseract.image_to_string(img)
                print('---------------------- Imagen a texto es ', texto)
                texto = texto.replace(',','')
            else:
                texto = ' '
                print('KKJJIHIKHNKH*YHIGIHKBJGHKBGHKBHK')
        else:
            print(' no conseguimos una url')
            texto = ' '
        
        print('////////', campos)
        campos[8] = texto.strip()
        print('////////', campos)
        linea = ','.join(campos)

        archivo_final.write(linea)


    archivo_final.close()
    archivo_csv.close()


# img = Image.open(f'./imagenes_telefonos/imagen{0}.jpg')
# texto = pytesseract.image_to_string(img)

# print(texto)