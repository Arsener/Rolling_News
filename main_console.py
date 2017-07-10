# encoding: utf-8
from  Child_news_scrapy import Sina_news_scrapy, NetEase_news_scrapy, Sohu_news_scrapy
import scrapy_handler
import MongoDB
from config import *
class Console():

    def construct_url_pic(self,web_list):  #构建url池
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
        return web_list

    def func(self,url):  #每个线程的工作函数
        if url == 'Sina':
            sina = Sina_news_scrapy()
            url = sina.url_construct()
            print(url)
            sina.url_request(url)
            data = sina.get_data()
            MongoDB.MongoDB.store('Sina', data)
        elif url == 'NetEase':
            netease = NetEase_news_scrapy()
            url = netease.url_construct()
            netease.url_request(url)
            data = netease.get_data()
            MongoDB.MongoDB.store('NetEase', data)
        elif url == 'sohu':
            sohu = Sohu_news_scrapy()
            url = sohu.url_construct()
            sohu.url_request(url)
            data = sohu.get_data()
            MongoDB.MongoDB.store('sohu', data)

    def mlti_thread(self,url_pool):        #多线程处理
        numthread = NUMTHREAD
        s=scrapy_handler.ScrapyHandler(url_pool,numthread,self.func)
        s.wait_allfinish()

# url_pool = Console.construct_url_pic(Console(),['Sina', 'NetEase', 'sohu'])



