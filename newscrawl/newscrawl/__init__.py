import pymongo
import json

def load_key(key_file) :
    with open(key_file) as key_file :
        key = json.load(key_file)
    return key

class MongoDB :
    # mongo = load_key(key_file='/home/keyog/coding/main-news-analys/localhost_mongo_key.json')
    mongodb = pymongo.MongoClient(f"mongodb://172.16.103.135:27017")
    @classmethod
    def conn_mongodb(cls,db_name) :
        try:
            cls.mongodb.admin.command('ismaster')
            collection = cls.mongodb.newscrawl[f'{db_name}']
        except :
            cls.mongodb = pymongo.MongoClient(f"mongodb://172.16.103.135:27017")
            collection = cls.mongodb.newscrawl[f'{db_name}']
        return collection
