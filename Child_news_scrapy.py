# encoding: utf-8
import random,time,json
import MongoDB
from urllib.parse import urlencode
from News_scrapy import News_scrapy
from Requests_c import Requests_c

class Sina_news_scrapy(News_scrapy):
    name = 'Sina'

    def __init__(self):
        super(Sina_news_scrapy,self).__init__(self.name)
        self.last_time=int(time.time())-60  #每次都改变


    def url_construct(self):
        url_param={
              "col":90,
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
        url_param['last_time']=str(self.last_time)
        url="http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php?"+urlencode(url_param)
        print('===')
        print(url)
        print('===')
        return url



    def get_data(self):
        print(type(self.first_data))
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
        if list:
            self.last_time = list[0]['time']
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
    name = 'sohu'

    def __init__(self):
        super(Sohu_news_scrapy,self).__init__(self.name)
        pass

    def url_construct(self):
        today = time.strftime('%Y-%m-%d', time.localtime())
        today = today.replace('-', '')
        url= "http://news.sohu.com/_scroll_newslist/" + today + "/news.inc"
        return url

    def get_data(self):
        self.first_data.encoding='utf-8'
        t = self.first_data.text[16:]
        t = t.replace('category', '\"category\"')
        t = t.replace('item', '\"item\"')
        te = json.loads(t)
        year = time.strftime('%Y', time.localtime())

        latest = MongoDB.MongoDB.get_latest(self.name)
        latest_title = latest.get('title')

        data = []
        for item in te['item']:
            if item[1] == latest_title:
                break

            dict = {}
            dict['title'] = item[1]
            dict['url'] = item[2]
            item[3] = '' + item[3].replace('/', '-')
            item[3] = year + '-' + item[3]
            dict['time'] = item[3]
            data.append(dict)
        return  data

class NetEase_news_scrapy(News_scrapy):
    name = 'NetEase'

    def __init__(self):
        super(NetEase_news_scrapy,self).__init__(self.name)
        pass

    def url_construct(self):
        url= "http://news.163.com/special/0001220O/news_json.js?"+str(random.random())
        return url

    def get_data(self):
        t = self.first_data.text
        t = t[9:len(t)-1]

        latest = MongoDB.MongoDB.get_latest(self.name)
        latest_title = latest.get('title')
        news_list = json.loads(t).get("news")[0]

        data = []
        for news in news_list:
            if news.get('t') == latest_title:
                break

            title = news.get('t')
            url = news.get('l')
            news_time = news.get('p')

            dict = {}
            dict['title'] = title
            dict['url'] = url
            dict['time'] = news_time
            data.append(dict)

        return data





