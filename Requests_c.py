# encoding: utf-8
import requests
import mylog
class Requests_c (object):
    '''
    recept url,handle the wrong data and return right data
    '''
    def __init__(self,url):
        self.url=url

    def url_handler(self):
        try:
            re=requests.get(self.url)
            if re.status_code==200:
                firstdata=re
                print('Right request ' + str(self.url))
                mylog.logInfo('request %s success' %str(self.url))
                return firstdata   #response类型
            else:
                print(re.status_code+' error')
                return None
        except Exception as e:
            print(str(e))
        finally:
            pass





