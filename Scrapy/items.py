# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    company = scrapy.Field()
    city = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    currency = scrapy.Field()
    link = scrapy.Field()
