# encoding: utf-8
import requests
class Requests_c (object):
    '''
    recept url,handle the wrong data and return right data
    '''
    def __init__(self,url):
        self.url=url

    def url_handler(self,url):
        try:
            re=requests.get(url)
            if re.status_code==200:
                firstdata=re
                print('Right request ' + url)
                return firstdata
            else:
                print(re.status_code+' error')
                return None
        except Exception as e:
            print(str(e))
        finally:
            pass





