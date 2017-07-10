from pymongo import MongoClient
import json

#实现对数据库类的封装
class MongoDB(object):
    __db = None

    @classmethod
    def store(cls, web_name, new_data):
        if len(new_data) == 0:
            print('empty')
            return

        if cls.__db is None:
            client = MongoClient('127.0.0.1', 27017)
            cls.__db = client.news_list
            print("new connect to news_list")

        exist = cls.__db.news_cla.find_one({"from": web_name})
        if exist is None:
            cls.__db.news_cla.insert({"from": web_name, "data": []})
            print('create a new base info')

        # cls.__db.news_cla.remove()
        # for item in cls.__db.news_cla.find():
        #     print(item)

        new_data.reverse()
        # if len(latest) == 0:
        for data in new_data:
            cls.__db.news_cla.update({"from": web_name}, {'$push': {"data": data}})

        # cls.__db.news_cla.remove()
        for item in cls.__db.news_cla.find():
            print(item)

    @classmethod
    def get_latest(cls, web_name):
        if cls.__db is None:
            client = MongoClient('127.0.0.1', 27017)
            cls.__db = client.news_list
            print("new connect to news_list")

        latest = None
        for item in cls.__db.news_cla.find({'from': web_name}, {'data': {'$slice': [-1, 1]}}):
            latest = str(item)
        if latest is not None:
            return json.loads(latest.split('[')[1].split(']')[0].replace("'", '"'))
        else:
            return {'title':'none'}
