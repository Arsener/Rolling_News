from pymongo import MongoClient

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

        latest = None
        for item in cls.__db.news_cla.find({'from': web_name}, {'data': {'$slice': [-1, 1]}}):
            latest = str(item)

        latest = latest.split('[')[1]
        latest = latest.split(']')[0]
        # print(latest)

        new_data.reverse()
        if len(latest) == 0:
            for data in new_data:
                cls.__db.news_cla.update({"from": web_name}, {'$push': {"data": data}})
        else:
            flag = False
            for data in new_data:
                str_data = str(data).replace('"', "'")
                if str_data == latest:
                    flag = True
                    break
            if flag == False:
                for data in new_data:
                    cls.__db.news_cla.update({"from": web_name}, {'$push': {"data": data}})
            else:
                save = False
                for data in new_data:
                    str_data = str(data).replace('"', "'")
                    if str_data == latest:
                        save = True
                        continue
                    elif save == True:
                        cls.__db.news_cla.update({"from": web_name}, {'$push': {"data": data}})

        # cls.__db.news_cla.remove()
        # for item in cls.__db.news_cla.find():
        #     print(item)

    # def get_latest(self, web_name):
    #     latest = None
    #     for item in self.__db.news_cla.find({'from': web_name}, {'data': {'$slice': [-1, 1]}}):
    #         latest = str(item)
    #
    #     latest = latest.split('[')[1]
    #     latest = latest.split(']')[0]
    #     # print(latest)
    #     return latest
