from elasticsearch import Elasticsearch
import mylog,time
from config import *
from elasticsearch.exceptions import TransportError
#对elasticsearch数据库的操作
class ElasticSearch(object):
    __es=None

    @classmethod
    def store(cls, web_name, new_data):
        if len(new_data) == 0:
            mylog.logInfo('%s:new data is none'%web_name)
            return

        if cls.__es is None:
            cls.__es = Elasticsearch([ELASTICSEARCH_URL], http_auth=('elastic', 'changeme'), port=ELASTICSEARCH_PORT)
            mylog.logInfo("store:new connect to "+ELASTICSEARCH_NEWS_INDEX)

        #插入更新last-time
        body = {}
        doc=new_data[0]
        count=0
        exist=cls.__es.exists(index=ELASTICSEARCH_NEWS_INDEX, doc_type=ELASTICSEARCH_NEWS_TYPE_OF_LAST_TIME, id=web_name)
        if exist:
            res=cls.__es.get(index=ELASTICSEARCH_NEWS_INDEX, doc_type=ELASTICSEARCH_NEWS_TYPE_OF_LAST_TIME, id=web_name)
            num=int(res['_source']['num'])
            doc['num']=len(new_data)+num
            count=num
            body['doc']=doc
            cls.__es.update(index=ELASTICSEARCH_NEWS_INDEX, doc_type=ELASTICSEARCH_NEWS_TYPE_OF_LAST_TIME, id=web_name,
                            body=body)
        else:
            doc['num']=len(new_data)
            body=doc
            cls.__es.index(index=ELASTICSEARCH_NEWS_INDEX, doc_type=ELASTICSEARCH_NEWS_TYPE_OF_LAST_TIME, id=web_name,
                           body=body)

        mylog.logInfo('%s:update new last_time success' % web_name)
        new_data[0].pop('num')
        #存储数据
        for i in range(len(new_data)):
            new_data[i]['from']=web_name
            st = time.strptime(new_data[i]['time'], '%Y-%m-%d %H:%M:%S')
            new_data[i]['time_num']=int(time.mktime(st))
            cls.__es.index(index=ELASTICSEARCH_NEWS_INDEX, doc_type=ELASTICSEARCH_NEWS_TYPE_OF_INFO, body=new_data[i])
        mylog.logInfo('%s:store new data success' % web_name)


    @classmethod
    def get_latest(cls, web_name):

        if cls.__es is None:
            cls.__es = Elasticsearch([ELASTICSEARCH_URL], http_auth=('elastic', 'changeme'), port=ELASTICSEARCH_PORT)
            mylog.logInfo("get_latest:new connect to " + ELASTICSEARCH_NEWS_INDEX)

        exist = cls.__es.exists(index=ELASTICSEARCH_NEWS_INDEX, doc_type=ELASTICSEARCH_NEWS_TYPE_OF_LAST_TIME,
                                id=web_name)
        if exist:
            res=cls.__es.get(index=ELASTICSEARCH_NEWS_INDEX, doc_type=ELASTICSEARCH_NEWS_TYPE_OF_LAST_TIME,
                             id=web_name)
            return res['_source']
        else:
            return {'title':'none'}
