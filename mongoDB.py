from pymongo import MongoClient
import json
from config import *
import mylog
#实现对数据库类的封装
class MongoDB(object):
    __db = None

    @classmethod
    def store(cls, web_name, new_data):
        if len(new_data) == 0:
            mylog.logInfo('%s:new data is none'%web_name)
            return

        if cls.__db is None:
            client = MongoClient(MONGO_URL, MONGO_PORT)
            cls.__db = client[MONGO_DB]
            mylog.logInfo("store:new connect to "+MONGO_DB)

        exist = cls.__db[MONGO_TABLE].find_one({"from": web_name})
        if exist is None:
            cls.__db[MONGO_TABLE].insert({"from": web_name, "data": []})
            mylog.logInfo('%s:create a new base info'%web_name)

        # cls.__db.news_cla.remove()
        # for item in cls.__db.news_cla.find():
        #     print(item)

        new_data.reverse()
        # if len(latest) == 0:
        for data in new_data:
            cls.__db[MONGO_TABLE].update({"from": web_name}, {'$push': {"data": data}})

        mylog.logInfo('%s:store new data success' % web_name)
        # cls.__db.news_cla.remove()
        # for item in cls.__db[MONGO_TABLE].find():
        #     print(item)


    @classmethod
    def get_latest(cls, web_name):
        if cls.__db is None:
            client = MongoClient(MONGO_URL, MONGO_PORT)
            cls.__db = client[MONGO_DB]
            mylog.logInfo("get_latest:new connect to "+MONGO_DB)

        latest = None
        for item in cls.__db[MONGO_TABLE].find({'from': web_name}, {'data': {'$slice': [-1, 1]}}):
            latest = str(item)
        if latest is not None:
            return json.loads(latest.split('[')[1].split(']')[0].replace("'", '"'))
        else:
            return {'title':'none'}
