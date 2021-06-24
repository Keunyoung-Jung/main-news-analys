# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime
from newscrawl import MongoDB


class NewscrawlPipeline:
    def process_item(self, item, spider):
        collection = MongoDB.conn_mongodb(spider.name)
        collection.insert_one(item).inserted_id
        return item
