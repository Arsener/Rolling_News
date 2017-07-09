# encoding: utf-8
import random,time,json
from urllib.parse import urlencode
from News_scrapy import News_scrapy
from Requests_c import Requests_c

class Sina_news_scrapy(News_scrapy):

    def __init__(self):
        self.last_time=int(time.time())  #每次都改变

    def url_contruct(self):
        url_param={
              "col":89,
              "spec":'',
              "date":'',     #第一次打开无此参数，以后每次刷新有这个参数
              "ch":'01',
              "k":'',
              "offset_page":0,
              "offset_num":0,
              "num":60,
              "asc":'',
              "page":1,
              "last_time":'', #第一次打开无此参数，以后每次刷新有这个参数
              "r":''
        }
        url_param['r']=random.random()
        url_param['last_time']=self.last_time
        url="http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php?"+urlencode(url_param)
        return url



    def get_data(self):
        self.first_data.encoding = 'gbk'
        t = self.first_data.text[15:-1]
        t = t.replace('serverSeconds', '\"serverSeconds\"')
        t = t.replace('path', '\"path\"')
        t = t.replace('count', '\"count\"')
        t = t.replace('offset_page', '\"offset_page\"')
        t = t.replace('offset_num', '\"offset_num\"')
        t = t.replace('title', '\"title\"')
        t = t.replace('list', '\"list\"')
        t = t.replace('id', '\"id\"')
        t = t.replace('cType', '\"cType\"')
        t = t.replace('channel', '\"channel\"')
        t = t.replace('url', '\"url\"')
        t = t.replace('type', '\"type\"')
        t = t.replace('pic', '\"pic\"')
        t = t.replace('time', '\"time\"')
        t = t.replace('last_\"time\"', '\"last_time\"')
        t = t.replace('\'', '\"')
        js = json.loads(t)
        list=js['list']
        data=[]
        for i in range(len(list)):
            list[i].pop('channel')
            list[i].pop('type')
            list[i].pop('pic')
            list[i]['time'] = time.localtime(list[i]['time'])
            list[i]['time'] = time.strftime("%Y-%m-%d %H:%M:%S", list[i]['time'])
            data.append(list[i])
        return data

class Sohu_news_scrapy(News_scrapy):

    def url_construct(self):
        today = time.strftime('%Y-%m-%d', time.localtime())
        today = today.replace('-', '')
        url= "http://news.sohu.com/_scroll_newslist/" + today + "/news.inc"
        return url

    def get_data(self):
        self.first_datar.encoding='utf-8'
        t = self.first_data.text[16:]
        t = t.replace('category', '\"category\"')
        t = t.replace('item', '\"item\"')
        te = json.loads(t)
        year = time.strftime('%Y', time.localtime())
        data = []
        for item in te['item']:
            dict = {}
            dict['title'] = item[1]
            dict['url'] = item[2]
            item[3] = '' + item[3].replace('/', '-')
            item[3] = year + '-' + item[3]
            dict['time'] = item[3]
            data.append(dict)
        return  data






