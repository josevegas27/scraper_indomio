import scrapy
import re


class Scraper1PySpider(scrapy.Spider):
    name = "scraper1"
    allowed_domains = ["www.indomio.es"]
    start_urls = ["https://www.indomio.es"]

    def parse(self,response):
        # Para la siguiente categoria
        enlace_next = response.xpath("//ul[@class='nd-tabBar nd-tabBar--compact hp-seoMap__tabBar']/li/a/@href").getall()[0:8]                  
        print(':::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::',enlace_next)
        print()

        for categ in enlace_next:

            url0 = response.urljoin(categ)

            yield scrapy.Request(url0,callback=self.parse0)

    def parse0(self, response):
        
        print()
        print()
        enlaces = response.xpath("//li[@class='hp-listMeta__item']/a/@href").getall()
        print(len(enlaces))
        for href in enlaces:

            url = response.urljoin(href)

            print(href)
            print("\n        Llamada a yiel principal \n")
            yield scrapy.Request(url, callback=self.parse_details)

        
        # if enlace_next != None:
        #     url3 = response.urljoin(enlace_a_next)

        #     yield scrapy.Request(url3,callback=self.parse_details2)


    def parse_details(self,response):

        enlaces2 = response.xpath("//a[@class='hp-listMeta__link']/@href").getall()

        print()
        print()
        # print(enlaces2)

        for eln in enlaces2:


            url2 = response.urljoin(eln)

            print(eln)
            print("\n        Llamada a yiel 2 \n")
            yield scrapy.Request(url2, callback=self.parse_details2)

    def parse_details2(self, response):

        #########################
        # Pasar de pagina si hay mas
        enlace_a_next =  response.xpath("//div[@class='in-pagination__list']/div[@class='nd-button nd-button--ghost in-pagination__item in-pagination__item--current']/following-sibling::*[1]/@href").get()
        # num_pag = response.xpath("//div[@class='in-pagination__list']/a/@href").getall()
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@',enlace_a_next)

        
        enlaces3 = response.xpath("//li[@class='nd-list__item in-searchLayoutListItem']/div/div/div[2]/a/@href").getall()

        for eln in enlaces3:

            url3 = response.urljoin(eln)
            print(eln)
            print("\n        Llamada a yiel 3 \n")
            yield scrapy.Request(url3, callback=self.parse_details3)
        

        if enlaces3 != None:
            url3 = response.urljoin(enlace_a_next)

            yield scrapy.Request(url3,callback=self.parse_details2)

        #   yield scrapy.Request(url_new, callback=self.parse_details4)



        

    def parse_details3(self, response):

        par1 = response.xpath("//dl/dt/text()").getall()
        par2 = response.xpath("//dl/dd")

        banos = 'desc'
        superficie = 'desc'
        contrato = 'desc'
        tipo = 'desc'
        habitaciones = [0,0]

        for name,value in zip(par1,par2):
            print('[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]',name)
            
            if name == 'superficie':
                sup = value.xpath("./text()").get()
                superficie = sup.split('|')[0]      #Para separa |

                print('++++++++++++++',sup)

            if name == 'contrato':
                sup = value.xpath("./text()").get()
                contrato = sup  



            if name == 'habitaciones':
                sup = value.xpath("./text()").get()
                sup = sup.split(',')
                sup = [hab.strip() for hab in sup]
                print('/////////////////////////////////////////////////////////', sup)

                

                for hab in sup:
                    
                    if 'baño' in hab:
                        
                        print('/////////////////////////////////////////////////////////', hab)
                        banos = hab
                        break
                
                habitaciones = [re.findall(r'[0-9]{0,2}[a-z]*[^\s]',hab)[0] for hab in sup]
                for i,hab in enumerate(habitaciones):
                    if re.findall(r'[^\d]\w*',hab) != []:
                        habitaciones[i] = 1
                    else:
                        habitaciones[i] = int(hab)

                print('========l=l=l=l=l=l=l=lll==l=',habitaciones)
                        
            
            if name == 'tipología' or name=='tipologia':
                sup = value.xpath("./text()").get()
                tipo = sup.split('|')[0]


        
        


        titulo = response.xpath("//h1[@class='re-title__title']/text()").get()
        municipio = response.xpath("//span[@class='re-title__location']/text()").get()
        # superficie = response.xpath("//div[@class='re-mainFeatures__item']/span/text()").get()
        precio = response.xpath("//div[@class='re-overview__price']/span/text()").get()
        
        
        vendedor = response.xpath("//div[@class='in-referent in-referent__withPhone']/a/p/text()").get()
        # eln_telf = response.xpath("//div[@class='in-referent in-referent__withPhone']/div/a/svg/use").get()[-15:-7]

        print('***************', superficie)
        print('---------------',precio)
        print('++++++++++++++',superficie)
        elnc = response.url

        # print(pares1)

        yield {
            "titulo":titulo,
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