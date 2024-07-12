import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager # type: ignore
from scrapy.selector import Selector
import time

class ExampleSpider(scrapy.Spider):
    name = 'example'

    def __init__(self, *args, **kwargs):
        super(ExampleSpider, self).__init__(*args, **kwargs)
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Ejecutar en modo headless (sin interfaz gráfica)
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def start_requests(self):
        urls = [
            'https://www.indomio.es/agencias-inmobiliarias'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.driver.get(response.url)

        time.sleep(1)
        # Aceptar cookies
        button_cookies = self.driver.find_element(By.XPATH, "//*[@id='didomi-notice-agree-button']")
        button_cookies.click()

        # Esperar hasta que el botón o enlace esté presente
        time.sleep(1)  # Ajusta el tiempo de espera según sea necesario

        href_provincias = response.xpath("//ul[@class='hp-listMeta hp-listMeta--columns']/li[@class='hp-listMeta__item']/a/@href").getall()

        for href in href_provincias[0:1]:
            url = response.urljoin(href)

            print(url)

            # yield scrapy.Request(url,callback=self.parse1)


    def parse1(self,response):

        href_municipios = response.xpath("//a[@class='hp-listMeta__link']/@href").getall()

        for href_mun in href_municipios[0:1]:
            url_mun = response.urljoin(href_mun)
            yield scrapy.Request(url_mun, callback=self.parse2)

    def parse_details2(self, response):

        href_anuncios = response.xpath("//li[@class='nd-list__item in-searchLayoutListItem']/div/div/div[2]/a/@href").getall()
        
        for href_anuncio in href_anuncios:
            url_anuncio = response.urljoin(href_anuncio)
            yield scrapy.Request(url_anuncio, callback=self.parse_details3)
               
        # Pasar de pagina si hay mas
        href_siguiente =  response.xpath("//div[@class='in-pagination__list']/div[@class='nd-button nd-button--ghost in-pagination__item in-pagination__item--current']/following-sibling::*[1]/@href").get()

        if href_siguiente != None:
            url_sig = response.urljoin(href_siguiente)
            yield scrapy.Request(url_sig,callback=self.parse_details2)


    def parse_details2(self,response):        
        # Encontrar el botón o enlace usando Selenium y hacer clic en él
        try:
            button = self.driver.find_element(By.XPATH, "//*[@id='layout-content']/section[2]/div/div/section/div/div/div/a")
            button.click()

            # Obtener el contenido de la nueva página después del clic
            time.sleep(5)  # Ajusta el tiempo de espera según sea necesario

            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            telf = self.driver.find_element(By.XPATH, "//*[@id='layout-content']/section[2]/div/div/section/div/div/div/a")
            
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", telf.text)

            yield {"telf":telf}
        except Exception as e:
            self.log(f'+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++Error: {e}')

        self.driver.quit()
