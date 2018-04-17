# -*- coding: utf-8 -*-

# Define here the models for scraped items

from scrapy import Item, Field

class RutItem(Item):
    title = Field()
    res_url = Field()
    uid = Field()
    author = Field()
    cover = Field()
    publisher = Field()
    pub_date = Field()
    language = Field()
    binding = Field()
