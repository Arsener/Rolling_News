# encoding: utf-8
import random,time,json
from urllib.parse import urlencode
from News_scrapy import News_scrapy
from Requests_c import Requests_c

class Sina_news_scrapy(News_scrapy):
    def get_data(self,name):
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
              "last_time":int(time.time()), #第一次打开无此参数，以后每次刷新有这个参数
              "r":0.1
        }
        url_param['r']=random.random()
        url_param['last_time']=last_time
        url="http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php?"+urlencode(url_param)
        re=Requests_c(url)
        first_data=re.url_handler(url)
        first_data.encoding='gbk'
        t=first_data.text[15:-1]
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






