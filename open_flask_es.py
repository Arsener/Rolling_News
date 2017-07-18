from flask import Flask,make_response
from elasticsearch import Elasticsearch
import time
import json

app = Flask(__name__)
es = Elasticsearch(['localhost'], http_auth=('elastic', 'changeme'), port=9200)   #5601

@app.route('/api/')
def hello_world():
    return 'Hello World!'

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'ok':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(str({'error': 'Unauthorized access'}), 401)



@app.route('/api/es')
@auth.login_required
def get_latest_news():
    result={}
    result['request_time'] = time.time()
    result['latest_news']=[]
    body = {
        "query": {"match_all": {}},
        "sort": [
            {"time_num": {"order": "desc"}}
        ]
    }
    res = es.search(index="my-news", doc_type="news-info", body=body)
    for news in res['hits']['hits']:
        news['_source'].pop('time_num')
        result['latest_news'].append(news['_source'])

    result=str(result).replace('\'','\"')
    return result

if __name__ == '__main__':
    app.run()