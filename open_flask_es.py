from flask import Flask,make_response,Response
from elasticsearch import Elasticsearch
import time
import json
import io,csv
import pandas as pd

app = Flask(__name__)
es = Elasticsearch(['localhost'], http_auth=('elastic', 'changeme'), port=9200)   #5601

@app.route('/api/')
def hello_world():
    return "Hello,world"

# data = [
#     ["REVIEW_DATE","AUTHOR","ISBN","DISCOUNTED_PRICE"],
#     ["1985/01/21","Douglas Adams",'0345391802',5.95],
#     ["1990/01/12","Douglas Hofstadter",'0465026567',9.95],
#     ["1998/07/15","Timothy \"The Parser\" Campbell",'0968411304',18.99],
#     ["1999/12/03","Richard Friedman",'0060630353',5.95],
#     ["2004/10/04","Randel Helms",'0879755725',4.50]
# ]
def get_latest_news_csv():
    request_time= time.time()
    data=[[],[],[],[],[],[],[],[],[],[],[]]
    data[0]=["request_time","title","url","time","from"]
    body = {
        "query": {"match_all": {}},
        "sort": [
            {"time_num": {"order": "desc"}}
        ]
    }
    res = es.search(index="my-news", doc_type="news-info", body=body)
    i=1
    for news in res['hits']['hits']:
        news['_source'].pop('time_num')
        data[i]=['','','','','']
        data[i][0]=request_time
        data[i][1]=news['_source']['title']
        data[i][2] = news['_source']['url']
        data[i][3] = news['_source']['time']
        data[i][4] = news['_source']['from']
        i+=1
    return data

@app.route('/download')
def download():
    si = io.StringIO()
    cw = csv.writer(si)
    data=get_latest_news_csv()
    cw.writerows(data)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output

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
#@auth.login_required
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