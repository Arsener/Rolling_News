# encoding: utf-8
import Requests_c
class News_scrapy(object):
    '''
    the parent of all the class
    '''
    def __init__(self,name):
        self.name=name         #name:从哪个门户
        self.first_data = ''   #从url_request中获得的原始数据response类型，需要在get_data中解析
        self.datas=''          #从get_data中获取，传递给filter_data和classify_data进一步处理


    def url_construct(self):   #每个子类中分别重写
        pass

    def url_request(self,url):
        re = Requests_c(url)
        self.first_data = re.url_handler()

    def get_data(self):   #每个子类中分别重写
        pass

    def filter_data(self):
        pass

    def classify_data(self):
        pass



