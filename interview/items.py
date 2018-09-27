# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class InterviewItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    date = scrapy.Field()
    major = scrapy.Field()
    location = scrapy.Field()
    numbers = scrapy.Field()
    website = scrapy.Field()

 #   email = scrapy.Field()
