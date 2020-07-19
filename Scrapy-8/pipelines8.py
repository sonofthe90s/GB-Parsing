from pymongo import MongoClient
import pymongo

class InstpagramparserPipeline:
    def __init__(self):
        # Если csv открыть файл на запись
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.inst_users_parser

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["inst_users_parser"]
mycol = mydb["instagram"]


subscribers = mycol.find({'username': 'fight_.wear', 'user_id_subscribers': {'$exists': True}},
                             {'info_full_user_name': 1, 'info_user_name': 1, })
print(f'Subscribers of fight_.wear user:')
for _, i in enumerate(subscribers):
    print(_, i)
print(subscribers)


follows = mycol.find({'username': 'fight_.wear', 'follow_by_user_id': {'$exists': True}},
                         {'info_full_user_name': 1, 'info_user_name': 1, })
print(f'Follows of fight_.wear user:')
for _, i in enumerate(follows):
    print(_, i)
print(follows)