# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from pymongo import MongoClient

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy_hh_scrapy

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]

        if spider.name == 'hhru':
            item['company'] = ' '.join(item['company']).replace("\xa0", "").replace("  ", " ")
            item['salary_min'] = int(item['salary_min'].replace("\xa0", ""))
            item['salary_max'] = int(item['salary_max'].replace("\xa0", ""))

        if spider.name == 'sjru':
            item['company'] = ' '.join(item['company']).replace("\xa0", "").replace("  ", " ")
            item['salary_min'] = int(item['salary_min'].replace("\xa0", ""))
            item['salary_max'] = int(item['salary_max'].replace("\xa0", ""))

        collection.insert_one(item)
        return item
