# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from time import strftime, localtime
class InterviewPipeline(object):
    def process_item(self, item, spider):
        item = dict(item)
    #    self.filter_item(item)
        self.store_item(item)
        
    def open_spider(self, spider):
        fname =  'whut_info' + strftime("%Y-%m-%d",localtime()) + '.txt'
        self.file =  open(fname, 'w', encoding='utf-8')
    
    def close_spider(self, spider):
        self.file.close()

    def store_item(self, item):
    #    self.filter_item(item)
        for key in item:
            if item[key] is None:
                item[key] = ''
            else :
                s = ''
                for ch in item[key]:
                    if ch != '\r' and ch != '\t' and ch != '\n':
                        s += ch
                item[key] = s
        
        line = ''
        for key in item:
            if item[key] is None: item[key] = ''
            line += key + ' : ' + str(item[key]) + '\n'
        line += '\n\n'
        print(line)
        self.file.write(line)
        

    def filter_item(self, item):
        #pass
        for key in item:
            if item[key] is None:
                item[key] = ''
            else :
                s = ''
                for ch in item[key]:
                    if ch != '\r' or ch != '\t' or ch != '\n':
                        s += ch
                item[key] = s