# encoding: utf-8
import requests
import json

url="http://localhost:5000/api/es"
s = requests.Session()
s.auth = ('ok', 'python')
s.headers.update({'x-test': 'true'})

# both 'x-test' and 'x-test2' are sent
re=s.get(url, headers={'x-test2': 'true'})
js=json.loads(re.text)
print(js['latest_news'])