# -*- encoding = utf-8 -*-
from flask import Flask, make_response, request
from flask_httpauth import HTTPBasicAuth
import mongoDB
import time
import json

app = Flask(__name__)
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'ok':
        return 'python'
    return None


@auth.error_handler
def unauthorized():
    return make_response(str({'error': 'Unauthorized access'}), 401)

	
@app.route('/api/latest_news', methods = ['POST'])
# @auth.login_required
def get_latest_news():
    if request.form.get('name') == 'arsener' and request.form.get('password') == '123':
        web_list = ['新浪','网易','腾讯','凤凰','搜狐']
        data = mongoDB.MongoDB.get_top10(web_list)
        data = sorted(data, key=lambda d: int(time.mktime(time.strptime(d['time'], "%Y-%m-%d %H:%M:%S"))))
        data.reverse()
        data = data[0:10]

        index_data = []
        for i in range(0, 10):
            tmp = str(data[i])
            tmp = tmp[0:7] + str(i) + tmp[7:]
            url_index = tmp.find("url")
            tmp = tmp[0:url_index + 3] + str(i) + tmp[url_index + 3:]
            time_index = tmp.find("time")
            tmp = tmp[0:time_index + 4] + str(i) + tmp[time_index + 4:]
            from_index = tmp.find("from")
            tmp = tmp[0:from_index + 4] + str(i) + tmp[from_index + 4:]
            tmp = tmp.replace("'", '"')
            tmp = tmp.replace('|','：')
            index_data.append(json.loads(tmp))
        return '{"request_time":' + str(time.time()) + ', "latest_news":' + str(index_data).replace("'", '"') + '}'
    else:
        return '{"request_time":-1}'

@app.route('/register', methods=['POST'])
def register():
    print(request.headers)
    print(request.form)
    print(request.form['name'])
    print(request.form.get('name'))
    print(request.form.getlist('name'))
    print(request.form.get('nickname', default='little apple'))
    return 'welcome'

# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == "__main__":
    app.run()
