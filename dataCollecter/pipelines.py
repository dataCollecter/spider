# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .store import data


class DataCollecterPipeline(object):
    def process_item(self, item, spider):
        data.update({'spider_name': item['spider_name'], 'url': item['url']}, {
                    '$set': dict(item)}, upsert=True)
        return item
