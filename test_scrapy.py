# encoding: utf-8
import requests
import json,time

url="http://localhost:5000/api/latest_news"
s = requests.Session()
s.auth = ('ok', 'python')

re = s.get(url)
print(re.text)
js=json.loads(re.text)
print(js['latest_news'])
