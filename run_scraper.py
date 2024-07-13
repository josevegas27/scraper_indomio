import os
import time

# print(os.getcwd())
# os.system('cd ./page_1')
# os.chdir(os.getcwd() + '/page_1')
print(os.getcwd())

# star_time = time.time()
# os.system('scrapy crawl venta -o ventas_alicante.csv')
# finish_time = time.time()

# print('Time:', finish_time - star_time)

categorias = [
        'Viviendas', 'Garajes', 'Edificios',
        'Oficinas', 'Locales', 'Actividades Comerciales',
        'Trasteros', 'Naves', 'Terrenos'
    ]

provincias = [
    "A Coruña",
    "Álava - Araba",
    "Albacete",
    "Alicante - Alacant",
    "Almería",
    "Andorra",
    "Asturias",
    "Ávila",
    "Badajoz",
    "Barcelona",
    "Burgos",
    "Cáceres",
    "Cádiz",
    "Cantabria",
    "Castellón - Castelló",
    "Ceuta",
    "Ciudad Real",
    "Córdoba",
    "Cuenca",
    "Gipuzkoa",
    "Girona",
    "Granada",
    "Guadalajara",
    "Huelva",
    "Huesca",
    "Islas Baleares",
    "Jaén",
    "La Rioja",
    "Las Palmas",
    "León",
    "Lleida",
    "Lugo",
    "Madrid",
    "Málaga",
    "Melilla",
    "Murcia",
    "Navarra",
    "Ourense",
    "Palencia",
    "Pontevedra",
    "Salamanca",
    "Santa Cruz de Tenerife",
    "Segovia",
    "Sevilla",
    "Soria",
    "Tarragona",
    "Teruel",
    "Toledo",
    "Valencia",
    "Valladolid",
    "Vizcaya - Bizkaia",
    "Zamora",
    "Zaragoza"
]

num_categorias = 9
num_provincias = 53


for i in range(num_categorias):

    for j in range(num_provincias):
        
        if input('Continuar con la siguiente provincia? (y/n)') == 'y':
            print()
            print(f"Ejecutando scraping de ventas de tipo {categorias[i]} en la provincia de {provincias[j]}")
            start_time = time.time()
            # os.system(f'scrapy crawl venta -o venta_catg{i}_prov{j}.csv -a categoria={i} -a provincia={j}')
            finish_time = time.time()
            print('#'*49)
            print(f'Scraping finalizado en {finish_time - start_time:.2f} segundos')
        else:
            
            


for i in range(num_categorias):

    for j in range(num_provincias):
        
        print()
        print(f"Ejecutando scraping de alquileres de tipo {categorias[i]} en la provincia de {provincias[j]}")
        start_time = time.time()
        # os.system(f'scrapy crawl alquiler -o alquiler_catg{i}_prov{j}.csv -a categoria={i} -a provincia={j}')
        finish_time = time.time()
        print(f'Scraping finalizado en {finish_time - start_time:.2f} segundos')

