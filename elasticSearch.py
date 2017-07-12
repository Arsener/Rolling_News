from elasticsearch import Elasticsearch
import mylog
from config import *
from elasticsearch.exceptions import TransportError
#对elasticsearch数据库的操作
class ElasticSearch(object):
    __es=None

    @classmethod
    def store(self,web_name,new_data):
        if len(new_data) == 0:
            mylog.logInfo('%s:new data is none'%web_name)
            return

        if self.__es is None:
            self.__es = Elasticsearch([ELASTICSEARCH_URL], http_auth=('elastic', 'changeme'), port=ELASTICSEARCH_PORT)
            mylog.logInfo("store:new connect to "+ELASTICSEARCH_NEWS_INDEX)

        try:
            q = {"query": {"match_all": {}}}
            res = self.__es.count(index=ELASTICSEARCH_NEWS_INDEX, doc_type=ELASTICSEARCH_NEWS_TYPE_OF_INFO, body=q)   #查询数据个数
            count=res['count']
        except TransportError:
            count=0

        for i in range(count,count+len(new_data)):
            new_data[i]['from']=web_name
            self.__es.index(index=ELASTICSEARCH_NEWS_INDEX, doc_type=ELASTICSEARCH_NEWS_TYPE_OF_INFO, id=int(i), body=new_data[i])

        mylog.logInfo('%s:store new data success' % web_name)

        #插入更新last-time
        body = {}
        exist=self.__es.exists(index=ELASTICSEARCH_NEWS_INDEX, doc_type=ELASTICSEARCH_NEWS_TYPE_OF_LAST_TIME, id=web_name)
        if exist:
            body['doc']=new_data[0]
            self.__es.update(index=ELASTICSEARCH_NEWS_INDEX, doc_type=ELASTICSEARCH_NEWS_TYPE_OF_LAST_TIME, id=web_name,
                       body=body)
        else:
            body=new_data[0]
            self.__es.index(index=ELASTICSEARCH_NEWS_INDEX, doc_type=ELASTICSEARCH_NEWS_TYPE_OF_LAST_TIME, id=web_name,
                       body=body)

        mylog.logInfo('%s:update new last_time success' % web_name)

    @classmethod
    def get_latest(self, web_name):

        if self.__es is None:
            self.__es = Elasticsearch([ELASTICSEARCH_URL], http_auth=('elastic', 'changeme'), port=ELASTICSEARCH_PORT)
            mylog.logInfo("get_latest:new connect to " + ELASTICSEARCH_NEWS_INDEX)

        exist = self.__es.exists(index=ELASTICSEARCH_NEWS_INDEX, doc_type=ELASTICSEARCH_NEWS_TYPE_OF_LAST_TIME,
                           id=web_name)
        if exist:
            res=self.__es.get(index=ELASTICSEARCH_NEWS_INDEX, doc_type=ELASTICSEARCH_NEWS_TYPE_OF_LAST_TIME,
                        id=web_name)
            return res['_source']
        else:
            return {'title':'none'}
