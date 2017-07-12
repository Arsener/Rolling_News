from elasticsearch import Elasticsearch
import mylog,time
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

        #插入更新last-time
        body = {}
        doc=new_data[0]
        count=0
        exist=self.__es.exists(index=ELASTICSEARCH_NEWS_INDEX, doc_type=ELASTICSEARCH_NEWS_TYPE_OF_LAST_TIME, id=web_name)
        if exist:
            res=self.__es.get(index=ELASTICSEARCH_NEWS_INDEX, doc_type=ELASTICSEARCH_NEWS_TYPE_OF_LAST_TIME,id=web_name)
            num=int(res['_source']['num'])
            doc['num']=len(new_data)+num
            count=num
            body['doc']=doc
            self.__es.update(index=ELASTICSEARCH_NEWS_INDEX, doc_type=ELASTICSEARCH_NEWS_TYPE_OF_LAST_TIME, id=web_name,
                       body=body)
        else:
            doc['num']=len(new_data)
            body=doc
            self.__es.index(index=ELASTICSEARCH_NEWS_INDEX, doc_type=ELASTICSEARCH_NEWS_TYPE_OF_LAST_TIME, id=web_name,
                       body=body)

        mylog.logInfo('%s:update new last_time success' % web_name)

        #存储数据

        for i in range(len(new_data)):
            new_data[i]['from']=web_name
            self.__es.index(index=ELASTICSEARCH_NEWS_INDEX, doc_type=ELASTICSEARCH_NEWS_TYPE_OF_INFO, id=web_name+str(i+count), body=new_data[i])
        mylog.logInfo('%s:store new data success' % web_name)


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
