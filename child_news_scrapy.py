# encoding: utf-8
import random,time,json
import mongoDB,elasticSearch
from urllib.parse import urlencode
from news_scrapy import News_scrapy
from bs4 import BeautifulSoup
from requests_c import Requests_c
import re

class Sina_news_scrapy(News_scrapy):
    name = 'Sina'

    def __init__(self):
        super(Sina_news_scrapy,self).__init__(self.name)
        self.last_time=int(time.time())-43200  #第一次运行先获取12小时之前到现在的所有news


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
        latest = mongoDB.MongoDB.get_latest(self.name)
        # latest = elasticSearch.ElasticSearch.get_latest(self.name)
        if latest['title']=='none':
            url_param['last_time'] = str(self.last_time)
        else:
            url_param['last_time'] = int(time.mktime(time.strptime(latest['time'],'%Y-%m-%d %H:%M:%S')))
        url="http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php?"+urlencode(url_param)
        return url

    def get_data(self):
        self.first_data.encoding = 'gbk'
        t = self.first_data.text[15:-1]
        titles = re.compile('},title : "(.*?)",url :').findall(t)
        urls = re.compile('"http://news.sina.com.cn/(.*?).shtml').findall(t)
        times = re.compile('time : (.*?)}').findall(t)
        data = []
        for i in range(len(titles)):
            list = {}
            list['title'] = titles[i]
            list['url'] = 'http://news.sina.com.cn/' + urls[i] + '.shtml'
            list['time'] = time.localtime(int(times[i]))
            list['time'] = time.strftime("%Y-%m-%d %H:%M:%S", list['time'])
            data.append(list)
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

        latest = mongoDB.MongoDB.get_latest(self.name)
        # latest = elasticSearch.ElasticSearch.get_latest(self.name)
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
            dict['time'] = item[3] + ':00'
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

        latest = mongoDB.MongoDB.get_latest(self.name)
        # latest = elasticSearch.ElasticSearch.get_latest(self.name)
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


class Tencent_news_scrapy(News_scrapy):
    name = 'Tencent'

    def __init__(self):
        super(Tencent_news_scrapy,self).__init__(self.name)
        pass

    def url_construct(self):
        url = "http://roll.news.qq.com/interface/roll.php?0.1&cata=newsgn&site=news&date=&page=1&mode=1&of=json"
        headers = {
            'Host': 'roll.news.qq.com',
            'Referer': 'http://roll.news.qq.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
        }
        return url,headers

    def get_data(self):
        js = json.loads(self.first_data.text)
        info = js['data']['article_info']
        titles = re.compile('.htm">(.*?)</a></li>').findall(info)
        urls = re.compile('</span><a target="_blank" href="(.*?)">').findall(info)
        times = re.compile('<span class="t-time">(.*?)</span><span class="t-tit">').findall(info)

        latest = mongoDB.MongoDB.get_latest(self.name)
        # latest = elasticSearch.ElasticSearch.get_latest(self.name)
        latest_title = latest.get('title')

        data = []
        year = time.strftime('%Y', time.localtime())
        for i in range(len(titles)):
            dict = {}
            if titles[i] ==latest_title:
                break
            dict['title'] = titles[i]
            dict['url'] = urls[i]
            dict['time'] = year + '-' + times[i] + ':00'
            data.append(dict)
        return data

class Ifeng_news_scrapy(News_scrapy):
    name = 'ifeng'

    def __init__(self):
        super(Ifeng_news_scrapy,self).__init__(self.name)
        pass

    def url_construct(self):
        url= "http://news.ifeng.com/listpage/11528/0/1/rtlist.shtml"
        return url

    def get_data(self):
        t = self.first_data.text
        bsObj = BeautifulSoup(t,'html.parser')
        #http://news.ifeng.com/a/20170710/51407729_0.shtml
        news_list = bsObj.find('div', {'class' : 'newsList'}).find_all('li')

        latest = mongoDB.MongoDB.get_latest(self.name)
        # latest = elasticSearch.ElasticSearch.get_latest(self.name)
        latest_title = latest.get('title')

        data = []
        for news in news_list:
            detail = news.find('a')
            if detail.get_text() == latest_title:
                break

            title = detail.get_text()
            url = detail['href']
            news_time = news.find('h4').get_text()
            news_time = '2017-' + news_time.replace('/', '-')

            dict = {}
            dict['title'] = title
            dict['url'] = url
            dict['time'] = news_time + ":00"
            data.append(dict)

        return data



