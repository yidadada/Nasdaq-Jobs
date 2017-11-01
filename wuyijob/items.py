# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class jobitems(scrapy.Item):
    url = scrapy.Field()
    position = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()
    salary = scrapy.Field()
    time = scrapy.Field()
    job_duty = scrapy.Field()


