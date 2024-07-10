import scrapy


class Scraper2Spider(scrapy.Spider):
    name = "scraper2"
    allowed_domains = ["www.yaencontre.com"]
    start_urls = ["https://www.yaencontre.com"]

    def parse(self, response):
        a = response.url
        print()
        print()
        print(a)
        yield a
