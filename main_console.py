# encoding: utf-8
from  child_news_scrapy import *
import scrapy_handler
import threading
import mongoDB
from config import *

class Console():

    def construct_url_pic(self,web_list):  #构建url池
        pass
        # url_pool=[]
        # for list in web_list:
        #     if list=='Sina':
        #         sina=Sina_news_scrapy()
        #         url=sina.url_contruct()
        #         url_pool.append(url)
        #     elif list == 'NetEase':
        #         netease = NetEase_news_scrapy()
        #         url = netease.url_construct()
        #         url_pool.append(url)
        #     elif list == 'sohu':
        #         sohu = Sohu_news_scrapy()
        #         url = sohu.url_construct()
        #         url_pool.append(url)
        #
        # return url_pool
        #return web_list

    def func(self,web_name):  #每个线程的工作函数
        lock=threading.Lock
        if web_name == 'Sina':
            sina = Sina_news_scrapy()
            url = sina.url_construct()
            sina.url_request(url,'')
            data = sina.get_data()
            #mongoDB.MongoDB.store('Sina', data)
            elasticSearch.ElasticSearch.store('Sina',data)
        elif web_name == 'NetEase':
            netease = NetEase_news_scrapy()
            url = netease.url_construct()
            netease.url_request(url,'')
            data = netease.get_data()
            #mongoDB.MongoDB.store('NetEase', data)
            elasticSearch.ElasticSearch.store('NetEase', data)
        elif web_name == 'sohu':
            sohu = Sohu_news_scrapy()
            url = sohu.url_construct()
            sohu.url_request(url,'')
            data = sohu.get_data()
            #mongoDB.MongoDB.store('sohu', data)
            elasticSearch.ElasticSearch.store('sohu', data)
        elif web_name == 'ifeng':
            ifeng = Ifeng_news_scrapy()
            url = ifeng.url_construct()
            ifeng.url_request(url,'')
            data = ifeng.get_data()
            #mongoDB.MongoDB.store('ifeng', data)
            elasticSearch.ElasticSearch.store('ifeng', data)
        elif web_name == 'Tencent':
            tencent= Tencent_news_scrapy()
            url,headers=tencent.url_construct()
            tencent.url_request(url,headers)
            data=tencent.get_data()
            #mongoDB.MongoDB.store('Tencent', data)
            elasticSearch.ElasticSearch.store('Tencent', data)

    def mlti_thread(self,web_list):        #多线程处理
        numthread = NUMTHREAD
        s=scrapy_handler.ScrapyHandler(web_list,numthread,self.func)
        s.wait_allfinish()

# url_pool = Console.construct_url_pic(Console(),['Sina', 'NetEase', 'sohu'])



