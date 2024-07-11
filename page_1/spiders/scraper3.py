import scrapy


class Scraper3Spider(scrapy.Spider):
    name = "scraper3"
    allowed_domains = ["www.indomio.es"]
    start_urls = ["https://www.indomio.es/alquiler-casas"]

    def parse(self, response):
        pass
