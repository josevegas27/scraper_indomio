import scrapy
import re


class Scraper1PySpider(scrapy.Spider):
    name = "alquiler"
    allowed_domains = ["www.indomio.es"]
    start_urls = ["https://www.indomio.es/alquiler-casas"]

    def parse(self,response):
        # Para la siguiente categoria
        enlace_next = response.xpath("//ul[@class='nd-tabBar nd-tabBar--compact hp-seoMap__tabBar']/li/a/@href").getall()[0:8]                  
        enlace_next[0] = "https://www.indomio.es/alquiler-casas/#map-list"
        
        for categ in enlace_next[0:1]:

            url0 = response.urljoin(categ)
            yield scrapy.Request(url0,callback=self.parse0)

    def parse0(self, response):
        
        enlaces = response.xpath("//li[@class='hp-listMeta__item']/a/@href").getall()
        for href in enlaces[0:1]:

            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse_details)


    def parse_details(self,response):

        enlaces2 = response.xpath("//a[@class='hp-listMeta__link']/@href").getall()

        for eln in enlaces2[0:1]:

            url2 = response.urljoin(eln)
            yield scrapy.Request(url2, callback=self.parse_details2)

    def parse_details2(self, response):

        #########################
        # Pasar de pagina si hay mas
        enlace_a_next =  response.xpath("//div[@class='in-pagination__list']/div[@class='nd-button nd-button--ghost in-pagination__item in-pagination__item--current']/following-sibling::*[1]/@href").get()
       
        enlaces3 = response.xpath("//li[@class='nd-list__item in-searchLayoutListItem']/div/div/div[2]/a/@href").getall()

        for eln in enlaces3[0:5]:

            url3 = response.urljoin(eln)
            yield scrapy.Request(url3, callback=self.parse_details3)
        

        if enlaces3 != None:
            url3 = response.urljoin(enlace_a_next)

            yield scrapy.Request(url3,callback=self.parse_details2)
  

    def parse_details3(self, response):

        par1 = response.xpath("//dl/dt/text()").getall()
        par2 = response.xpath("//dl/dd")

        banos = 'desc'
        superficie = 'desc'
        contrato = 'desc'
        tipo = 'desc'
        habitaciones = [0,0]

        for name,value in zip(par1,par2):
            
            if name == 'superficie':
                sup = value.xpath("./text()").get()
                superficie = sup.split('|')[0]      #Para separa |

    
            elif name == 'contrato':
                sup = value.xpath("./text()").get()
                contrato = sup  



            elif name == 'habitaciones':
                sup = value.xpath("./text()").get()
                sup = sup.split(',')
                sup = [hab.strip() for hab in sup]
                

                for hab in sup:
                    
                    if 'baño' in hab:
                        banos = hab
                        break
                
                habitaciones = [re.findall(r'[0-9]{0,2}[a-z]*[^\s]',hab)[0] for hab in sup]
                for i,hab in enumerate(habitaciones):
                    if re.findall(r'[^\d]\w*',hab) != []:
                        habitaciones[i] = 1
                    else:
                        habitaciones[i] = int(hab)

            
            elif name == 'tipología' or name=='tipologia':
                sup = value.xpath("./text()").get()
                tipo = sup.split('|')[0]


        # titulo = response.xpath("//h1[@class='re-title__title']/text()").get()
        municipio = response.xpath("//span[@class='re-title__location']/text()").get()
        # superficie = response.xpath("//div[@class='re-mainFeatures__item']/span/text()").get()
        precio = response.xpath("//div[@class='re-overview__price']/span/text()").get()
        vendedor = response.xpath("//div[@class='in-referent in-referent__withPhone']/a/p/text()").get()
        # eln_telf = response.xpath("//div[@class='in-referent in-referent__withPhone']/div/a/svg/use").get()[-15:-7]
        elnc = response.url

        yield {
            # "titulo":titulo,
            "meters":superficie,
            "price":precio,
            "bathrooms":banos,
            "category":tipo,
            "link":elnc,
            "municipality":municipio,
            "operation":contrato,
            "owner":vendedor,
            "rooms":sum(habitaciones)
        }


    def parse_details4(self, response):
        pass