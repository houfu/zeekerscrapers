# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZeekerArticle(scrapy.Item):
    title = scrapy.Field()
    date_scraped = scrapy.Field()
    date_published = scrapy.Field()
    text = scrapy.Field()
    url = scrapy.Field()
