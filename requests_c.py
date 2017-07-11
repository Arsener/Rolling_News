# encoding: utf-8
import requests
import mylog
class Requests_c (object):
    '''
    recept url,handle the wrong data and return right data
    '''
    def __init__(self,url):
        self.url=url

    def url_handler(self,headers):
        try:
            if headers:
                re = requests.post(self.url, headers=headers)
            else:
                re=requests.get(self.url)
            if re.status_code==200:
                firstdata=re
                mylog.logInfo('Request %s success' %str(self.url))
                return firstdata   #response类型
            else:
                mylog.logInfo(str(self.url)+' '+re.status_code+'error')
                return None
        except Exception as e:
            mylog.logInfo(str(e))
        finally:
            pass





