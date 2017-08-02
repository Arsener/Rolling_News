# -*- encoding = utf-8 -*-
from flask import Flask, Blueprint, request
from mongoDB import MongoDB
import time
import json

app = Flask(__name__)

	
@app.route('/api/latest_news', methods = ['POST'])
# @auth.login_required
def get_latest_news():
    if request.form.get('name') == 'arsener' and request.form.get('password') == '123':
        web_list = ['新浪','网易','腾讯','凤凰','搜狐']
        data = MongoDB.get_top10(web_list)
        data = sorted(data, key=lambda d: int(time.mktime(time.strptime(d['time'], "%Y-%m-%d %H:%M:%S"))))
        data.reverse()
        data = data[0:10]

        index_data = []
        for i in range(0, 10):
            tmp = str(data[i])
            title_index = tmp.find("title")
            tmp = tmp[0:title_index + 5] + str(i) + tmp[title_index + 5:]
            url_index = tmp.find("url")
            tmp = tmp[0:url_index + 3] + str(i) + tmp[url_index + 3:]
            time_index = tmp.find("time")
            tmp = tmp[0:time_index + 4] + str(i) + tmp[time_index + 4:]
            from_index = tmp.find("from")
            tmp = tmp[0:from_index + 4] + str(i) + tmp[from_index + 4:]
            tmp = tmp.replace("'", '"')
            tmp = tmp.replace('|',':')
            index_data.append(json.loads(tmp))
        return '{"request_time":' + str(time.time()) + ', "latest_news":' + str(index_data).replace("'", '"') + '}'
    else:
        return '{"request_time":-1}'


if __name__ == "__main__":
    from werkzeug.contrib.fixers import ProxyFix

    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run()


# gunicorn -w 4 -b 127.0.0.1:8000 open_flask_mo:app