# -*- encoding = utf-8 -*-
from flask import Flask
import mongoDB
import time
app = Flask(__name__)

@app.route('/api/latest_news')
def get_latest_news():
    web_list = ['Sina', 'NetEase', 'Tencent', 'ifeng', 'sohu']
    data = mongoDB.MongoDB.get_top10(web_list)
    data = sorted(data, key=lambda d: int(time.mktime(time.strptime(d['time'], "%Y-%m-%d %H:%M:%S"))))
    data.reverse()
    data = data[0:9]
    return '{"request_time":' + str(time.time())+', "latest_news":'+str(data).replace("'",'"') + '}'

if __name__ == "__main__":
    app.run()