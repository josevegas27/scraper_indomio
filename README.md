# Scraping de Indomio.es

Este scraping se ha realizado con Scrapy. El unico spider es llamado Indomio (Esto es debido al nombre de la pagina a scrapear). Al ejecutar el spider, este genera un archivo csv (opcional) que contiene los datos de los anuncios de inmuebles que son publicados por particulares y no por una inmobiliaria. Este archivo contiene varios campos, pero cabe resaltar que en correspondiente a telefono `phone`, tiene el enlace a la imagen que proporciona la pagina para el numero (Pues no proporciona el texto con el numero). Luego, al ejecutar el script `convertir_imagenes.py` se cambias estas imagenes al texto respectivo.


## Pasos para ejecutar este scraper

- Ejecutar en la terminal, para generar el archivo csv con los datos. El nombre `inmueble.csv` es necesarios para que el siguiente paso funcione correctamente.
    '''
        scrapy crawl indomio -o inmuebles.csv
    '''

- Ejecutar el Script convertir_imagenes.py: Este se encarga de convertir las imagenes de cada anuncio al texto correspondiente.
    '''
        python convertir_imagenes.py
    '''

Se genera un archivo `data.csv` con los datos de los anuncios y con sus numeros de telefonos en lugar de los enlaces a sus imagenes.