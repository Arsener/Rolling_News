# encoding: utf-8
from  Child_news_scrapy import Sina_news_scrapy, NetEase_news_scrapy, Sohu_news_scrapy
import scrapy_handler

class Console():

    def construct_url_pic(self,web_list):  #构建url池
        url_pool=[]
        for list in web_list:
            if list=='Sina':
                sina=Sina_news_scrapy()
                url=sina.url_contruct()
                url_pool.append(url)
            elif list == 'NetEase':
                netease = NetEase_news_scrapy()
                url = netease.url_construct()
                url_pool.append(url)
            elif list == 'sohu':
                sohu = Sohu_news_scrapy()
                url = sohu.url_construct()
                url.pool.append(url)

        return url_pool


    def mlti_thread(self,url_pool):        #多线程处理
        pass


