# encoding: utf-8
import requests
import json

# url="http://localhost:5000/api/latest_news"
# s = requests.Session()
# s.auth = ('ok', 'python')
#
# re = s.get(url)
# print(re.text)
# js=json.loads(re.text)
# print(js['latest_news'])

user_info = {'name': 'arsener'}
r = requests.post("http://127.0.0.1:5000/api/latest_news", data=user_info)

print(r.text)