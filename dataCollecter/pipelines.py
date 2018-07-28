# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .store import lastest_data, data


class DataCollecterPipeline(object):
    def process_item(self, item, spider):
        if len(list(data.find({'spider': item['spider'], 'title': item['title'], 'date': item['date']}))) == 0:
            lastest_data.update({'spider': item['spider'], 'url': item['url']}, {
                '$set': dict(item)}, upsert=True)
            data.update({'spider': item['spider'], 'url': item['url']}, {
                '$set': dict(item)}, upsert=True)
            return None
