import scrapy
from page_1.items import ImagenItem # type: ignor
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
            yield scrapy.Request(url_categ,callback=self.categoria)


    def categoria(self, response):
        # Listar todos los enlaces de cada provincia a consultar
        href_provincias = response.xpath("//ul[@class='hp-listMeta hp-listMeta--columns']/li[@class='hp-listMeta__item']/a/@href").getall()
        # print('////////////////////////////////////////////////////////////////////////////',len(href_provincias))
        for href_prov in href_provincias[0:1]:
            url_prov = response.urljoin(href_prov)
            yield scrapy.Request(url_prov, callback=self.parse_details)


    def parse_details(self,response):

        href_municipios = response.xpath("//a[@class='hp-listMeta__link']/@href").getall()

        for href_mun in href_municipios[:]:
            url_mun = response.urljoin(href_mun)
            yield scrapy.Request(url_mun, callback=self.parse_details2)


    def parse_details2(self, response):

        href_anuncios = response.xpath("//li[@class='nd-list__item in-searchLayoutListItem']/div/div/div[2]/a/@href").getall()
        
        for href_anuncio in href_anuncios:
            url_anuncio = response.urljoin(href_anuncio)
            yield scrapy.Request(url_anuncio, callback=self.parse_details3)
               
        # Pasar de pagina si hay mas
        href_siguiente =  response.xpath("//div[@class='in-pagination__list']/div[@class='nd-button nd-button--ghost in-pagination__item in-pagination__item--current']/following-sibling::*[1]/@href").get()
        n_href_siguiente =  response.xpath("//div[@class='in-pagination__list']/div[@class='nd-button nd-button--ghost in-pagination__item in-pagination__item--current']/following-sibling::*[1]/text()").get()
        
        print('#####################################################################',n_href_siguiente)
        if href_siguiente != None:
            url_sig = response.urljoin(href_siguiente)
            yield scrapy.Request(url_sig,callback=self.parse_details2)



    def parse_details3(self, response):

        self.contador += 1
        print('//////////////////////////////////', self.contador)

        municipio = response.xpath("//span[@class='re-title__location']/text()").get()
        print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", municipio)



        # Verificar que es un vendedor partcular        
        vendedor = response.xpath("//div[@class='in-referent in-referent__withPhone']/a/p/text()").get()
        if vendedor == None:
            lb_particular = response.xpath("//div[@class='nd-mediaObject__content']/p/text()").get()
            lb_inmobiliaria = response.xpath("//div[@class='in-referent']").get()
            
            if lb_particular != None and lb_inmobiliaria == None:
                vendedor = lb_particular
                src_telf = response.xpath("//div[@class='nd-mediaObject__content']/p[2]/img/@src").get()
                
                foto = ImagenItem()
                foto['url_imagen'] = src_telf

                # yield foto



                caract_label = response.xpath("//dl/dt/text()").getall()
                caract_value = response.xpath("//dl/dd")

                banos = None
                superficie = None
                contrato = None
                tipolg = None
                num_habitaciones = [0,0]

                for name, value in zip(caract_label, caract_value):
                    
                    if name == 'superficie':
                        superf = value.xpath("./text()").get()
                        superficie = superf.split('|')[0]      #Para separa |
                        superficie = re.findall(r'\d+',superficie)[0]

                    elif name == 'contrato':
                        contrato = value.xpath("./text()").get()  

                    elif name == 'habitaciones':
                        text_habs = value.xpath("./text()").get()
                        text_habs = re.sub(r'\((.*)\)',' ',text_habs)
                        list_habs = text_habs.split(',')
                        habitaciones = [hab.strip() for hab in list_habs]

                        for hab in habitaciones:
                            
                            if 'baño' in hab:
                                banos =  re.findall(r'\d{1,2}',hab)[0]
                                break
                        
                        num_habitaciones = [re.findall(r'[0-9]{0,2}[a-z]*[^\s]',hab)[0] for hab in habitaciones]

                        for i,hab in enumerate(num_habitaciones):
                            if re.findall(r'[^\d]\w*[^+]',hab) != []:
                                num_habitaciones[i] = 1
                            else:
                                num_habitaciones[i] = int(re.findall(r'\d{1,2}',hab)[0])

                    
                    elif name == 'tipología' or name=='tipologia':
                        tipolg = value.xpath("./text()").get()
                        tipolg = tipolg.split('|')[0]


                list_zona = response.xpath("//div[@class='re-title__content']/a/span/text()").getall()

                if list_zona == []:
                    zona = None
                else:
                    if len(list_zona) == 1:
                        if list_zona[0] ==  municipio:
                            zona = None
                        else:
                            zona = list_zona[0]
                    else:
                        if list_zona[0] == municipio:
                            list_zona.pop(0)
                        
                        zona = ' - '.join(list_zona)

                titulo = response.xpath("//h1[@class='re-title__title']/text()").get()
                # titulo = titulo.replace(municipio,'')

                titulo = titulo.split(',')
                for text in titulo:
                    if municipio not in text and zona not in text:
                        zona += ' - ' + text
                    break
                        




                precio = response.xpath("//div[@class='re-overview__price']/span/text()").get()
                precio =  re.findall(r'(\d+\.\d+)', precio)
                
                # eln_telf = response.xpath("//div[@class='in-referent in-referent__withPhone']/div/a/svg/use").get()[-15:-7]
                link = response.url

                yield {
                    "meters": superficie,
                    "price": precio,
                    "bathrooms": banos,
                    "category": tipolg,
                    "link": link,
                    "municipality": municipio,
                    "operation": contrato,
                    "owner": vendedor,
                    "phone": src_telf,
                    "rooms": sum(num_habitaciones) if sum(num_habitaciones) != 0 else None,
                    "zone": zona
                }


    
