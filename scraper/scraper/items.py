# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    name = scrapy.Field()
    ratings = scrapy.Field()
    country = scrapy.Field()
    genres = scrapy.Field()
    time = scrapy.Field()
