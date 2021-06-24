import pymongo
import json

def load_key(key_file) :
    with open(key_file) as key_file :
        key = json.load(key_file)
    return key

class MongoDB :
    mongo = load_key(key_file='/home/keyog/coding/main-news-analys/localhost_mongo_key.json')
    mongodb = pymongo.MongoClient(f"mongodb://{mongo['host']}:{mongo['port']}",
                                    username=mongo['user'],password=mongo['password'])
    @classmethod
    def conn_mongodb(cls,db_name) :
        try:
            cls.mongodb.admin.command('ismaster')
            collection = cls.mongodb.newscrawl[f'{db_name}']
        except :
            cls.mongodb = pymongo.MongoClient(f"mongodb://{cls.mongo['host']}:{cls.mongo['port']}",
                                    username=cls.mongo['user'],password=cls.mongo['password'])
            collection = cls.mongodb.newscrawl[f'{db_name}']
        return collection