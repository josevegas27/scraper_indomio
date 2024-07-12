# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImagenItem(scrapy.Item):
    url_imagen = scrapy.Field()
    imagen = scrapy.Field()
