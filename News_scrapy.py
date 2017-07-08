# encoding: utf-8
class News_scrapy(object):
    '''
    the parent of all the class
    '''
    def __init__(self,name):
        self.name=name      #name:从哪个门户
        self.datas=''       #从get_data中获取，传递给filter_data和classify_data进一步处理

    def get_data(self,name):
        pass

    def filter_data(self):
        pass

    def classify_data(self):
        pass



