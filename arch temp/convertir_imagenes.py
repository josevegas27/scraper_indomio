
import easyocr

# Crear un lector de EasyOCR
reader = easyocr.Reader(['es'])  # Puedes añadir otros idiomas si es necesario, como ['es', 'en']

# Leer la imagen
image_path = './imagenes_telefonos/imagen.jpg'
result = reader.readtext(image_path)