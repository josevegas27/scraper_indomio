import scrapy
from scrapy.selector import Selector
import re


class Scraper1PySpider(scrapy.Spider):
    name = "venta"
    allowed_domains = ["www.indomio.es"]
    start_urls = ["https://www.indomio.es"]

    contador = 0

    def parse(self,response):

        # Listar todos los enlaces correspondientes a cada categoria de ventas
        href_categorias = response.xpath("//ul[@class='nd-tabBar nd-tabBar--compact hp-seoMap__tabBar']/li/a/@href").getall()[0:9]                  
        for categ in href_categorias[0:1]:
            url_categ = response.urljoin(categ)
            yield scrapy.Request(url_categ, callback=self.categoria)


    def categoria(self, response):

        # Listar todos los enlaces de cada provincia a consultar
        href_provincias = response.xpath("//ul[@class='hp-listMeta hp-listMeta--columns']/li[@class='hp-listMeta__item']/a/@href").getall()
        for href_prov in href_provincias[0:1]:   # primer provincia
            url_prov = response.urljoin(href_prov)
            yield scrapy.Request(url_prov, callback=self.provincia)


    def provincia(self,response):

        # Listar todos los enlaces a municipios
        href_municipios = response.xpath("//a[@class='hp-listMeta__link']/@href").getall()
        
        enlace_todos = response.xpath("//p[@class='hp-seoSiteMap__description']/a/@href").get()
        texto_enlace_todos = response.xpath("//p[@class='hp-seoSiteMap__description']/a/text()").get()
        numero_posts = re.findall(r'(\d{1,}\.*\d{0,})', texto_enlace_todos)[0]
        numero_posts = re.sub(r'\.*','', numero_posts)

        if int(numero_posts) < 2000:
            href_municipios = None

        if href_municipios == None or href_municipios == []:
            
            url_enlace = response.urljoin(enlace_todos)
            yield scrapy.Request(url_enlace, callback=self.municipio)
        else:
            for href_mun in href_municipios[0:1]:  #primer municipio
                url_mun = response.urljoin(href_mun)
                yield scrapy.Request(url_mun, callback=self.municipio)


    def municipio(self, response):

        # Listar los enlaces a cada anuncio en la pagina actual
        xpath_anuncio = "//div[@class='nd-mediaObject__content in-listingCardPropertyContent']"
        elm_anuncios = response.xpath(xpath_anuncio).getall()

        # Recorrer los anuncios
        for elm in elm_anuncios[0:1]:  # Primer anuncio
            elm = Selector(text=elm)

            # Anuncios que tienen inmobiliarias
            elem_inmobiliaria = elm.xpath(".//div[@class='nd-figure in-listingCardAgencyLogo']").get()

            if elem_inmobiliaria != None:                           # Si tiene el campo inmobiliaria 
                continue
            else:                                                   # Si no tiene el campo inmobiliaria es porque puede ser de un particular
                href_anuncio = elm.xpath(".//a/@href").get()
                url_anuncio = response.urljoin(href_anuncio)

                yield scrapy.Request(url_anuncio,callback=self.anuncio)

               
        # Obtener el enlace a la siguiente pagina si es que existe
        href_siguiente =  response.xpath("//div[@class='in-pagination__list']/div[@class='nd-button nd-button--ghost in-pagination__item in-pagination__item--current']/following-sibling::*[1]/@href").get()

        # Si existe el enlace a la siguiente pagina, se prosigue a volver a hacer lo mismo, pero en la siguiente pagina
        if href_siguiente != None:
            url_sig = response.urljoin(href_siguiente)
            yield scrapy.Request(url_sig, callback=self.municipio)


    def anuncio(self, response):

        # Verificar que es un vendedor partcular        
        vendedor = response.xpath("//div[@class='in-referent in-referent__withPhone']/a/p/text()").get()
        # Si no se obtiene nada de lo anterior es porque no es un anuncio de inmobiliaria, de lo contrario, no se extrae informacion
        if vendedor == None:
            # Se prosigue a conseguir el texto del campo donde se ubica el nombre del particular
            name_particular = response.xpath("//div[@class='nd-mediaObject__content']/p/text()").get() # nombre del particular
            sub_inmobiliaria = response.xpath("//div[@class='in-referent']").get()                     # campo de la inmobiliaria que esta debajo del campo correspondiente al anterior
            
            if sub_inmobiliaria == None:                                                               # Si no hay inmobiliaria, es porque es un vendedor particular
                vendedor = name_particular if name_particular != 'Particular' else None

                # Con los siguientes campos
                superficie = None

                precio = response.xpath("//div[@class='re-overview__price']/span/text()").get()

                if precio == None:
                    precio = response.xpath("//div[@class='re-overview__price is-lowered']/span/text()").get()

                precio =  re.findall(r'(\d+\.*\d*\s*.?\w*)', precio)[0]  
                precio = re.sub(r'\.','',precio)                                                       # Formateamos para dejar solo el numero

                banos = None
                contrato = None
                tipolg = None
                link = response.url
                text_municipio = response.xpath("//span[@class='re-title__location']/text()").get()
                src_telf = response.xpath("//div[@class='nd-mediaObject__content']/p[2]/img/@src").get()
                num_habitaciones = [0,0]

                # Caracteriticas del inmueble en la pagina
                caract_text = response.xpath("//dl/dt/text()").getall()
                caract_value = response.xpath("//dl/dd")

                for name, value in zip(caract_text, caract_value):
                    
                    if name == 'superficie':
                        superf = value.xpath("./text()").get()
                        superf = superf.split('|')[0]      #Para separar por |
                        superficie = re.findall(r'\d+\.*\d*', superf)[0]
                        superficie = re.sub(r'\.','', superficie)
                        
                    elif name == 'contrato':
                        contrato = value.xpath("./text()").get()  

                    elif name == 'habitaciones':
                        text_habs = value.xpath("./text()").get()
                        text_habs = re.sub(r'\((.*)\)',' ', text_habs)
                        list_habs = text_habs.split(',')
                        habitaciones = [hab.strip() for hab in list_habs]

                        for hab in habitaciones:
                            
                            if 'baño' in hab:
                                banos =  re.findall(r'\d{1,2}', hab)[0]
                                break
                        
                        num_habitaciones = [re.findall(r'[0-9]{0,2}[a-z]*[^\s]', hab)[0] for hab in habitaciones]

                        for i,hab in enumerate(num_habitaciones):
                            if re.findall(r'[^\d]\w*[^+]', hab) != []:
                                num_habitaciones[i] = 1
                            else:
                                num_habitaciones[i] = int(re.findall(r'\d{1,2}', hab)[0])

                    elif name == 'tipología' or name =='tipologia':
                        tipolg = value.xpath("./text()").get()
                        tipolg = tipolg.split('|')[0]


                list_zona = response.xpath("//div[@class='re-title__content']/a/span/text()").getall()

                if list_zona == []:
                    zona = None
                else:
                    if len(list_zona) == 1:
                        if list_zona[0] == text_municipio:
                            zona = None
                        else:
                            zona = list_zona[0]
                    else:
                        for i, _ in enumerate(list_zona):
                            if list_zona[i] == text_municipio:
                                list_zona.pop(i)
                        
                        zona = ' - '.join(list_zona)

                # Para completar informacion de zona
                # Se obtiene el titulo de la publicacion, que a veces tiene direccion de la zona
                titulo = response.xpath("//h1[@class='re-title__title']/text()").get()

                # Se crea una lista y se itera en ella descartando los valores que contengan el municipio o la direccion de la zona que ya hallamos
                list_titulo = titulo.split(',')

                if zona != None:

                    for text in list_titulo:
                        if (text_municipio not in text) and (text not in zona) and (tipolg not in text) and ('estado' not in text) and ('condiciones' not in text):
                            zona += ' - ' + text
                            break
                else:
                    for text in list_titulo:
                        if (text_municipio not in text) and (tipolg not in text) and 'estado' not in text and 'condiciones' not in text:
                            zona = text
                            break

                yield {
                    "meters": superficie,
                    "price": precio,
                    "bathrooms": banos,
                    "category": tipolg,
                    "link": link,
                    "municipality": text_municipio,
                    "operation": contrato,
                    "owner": vendedor,
                    "phone": src_telf,
                    "rooms": sum(num_habitaciones) if sum(num_habitaciones) != 0 else None,
                    "zone": zona
                }


    
