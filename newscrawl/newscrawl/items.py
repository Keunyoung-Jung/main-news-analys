# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewscrawlItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    press = scrapy.Field()
    write_time = scrapy.Field()
    section = scrapy.Field()
    keywords = scrapy.Field()
    crawl_time = scrapy.Field()
    _id = scrapy.Field()