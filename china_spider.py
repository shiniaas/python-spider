#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json
from lxml import etree
import xlwt
import time

header = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
         }
 
proxy = { 
            'http' : 'xxx'
        }

  
url0 = 'http://d.qianzhan.com'
url1 = '/xdata/list/xfyyy0yyIxPyywyy2xDxfd.html'

result = {'name':'中国宏观', 'href':'http://d.qianzhan.com/xdata/list/xfyyy0yyIxPyywyy2xDxfd.html', 'child':[], 'num':''}
# result = {'name':'中国宏观', 'href':'http://d.qianzhan.com/xdata/list/xCxnxBy9xX.html', 'child':[], 'num':''}

# t = open('china.txt', 'w')


count = 0
def Get_info(level, url, con):
    global count
    cnt = 5
    flag = 0
    while cnt > 0 and flag == 0:
        try:
            text = requests.get(url, headers = header, proxies = proxy).text
            html = BeautifulSoup(text, 'lxml')
            num = html.find('div', attrs = {'class':'search-result-tit'}).find_all('em')[2].get_text()
            #获取中国宏观的所有孩子
            child_all0 = html.find_all('div', attrs = {'class':'searchfilter_sub'})
            if len(child_all0) == level + 1:
                flag = 1
                return
            
            child_all = child_all0[level].find_all('a')

            #删除第一个即全部
            del(child_all[0])
           
            for i in child_all:
                t_dict = {'name':'', 'href':'', 'child':[], 'num':''}
                name = i.get_text()
                href = i.get('href')
                t_dict['name'] = name
                t_dict['href'] = url0 + href
                con['child'].append(t_dict)
                count += 1
                print count, level, name , t_dict['href']
                Get_info(level + 1, t_dict['href'], con['child'][-1])
                flag = 1
            flag = 1
        except:
            time.sleep(1)
            cnt -= 1
    if flag == 0:
        print 'fail' + url
    
Get_info(0, result['href'], result)

f = open('fuck.txt', 'w')
f.write(str(result))

from pymongo import MongoClient
client = MongoClient('localhost', 27017)

db = client['china']

text = result
cur_id = 1

def import_to_mongodb(data, parentid):
    global cur_id
    for i in data:
        insert_info1 = {}
        insert_info1['id'] = cur_id
        cur_id += 1
        print cur_id
        insert_info1['parentid'] = parentid
        insert_info1['name'] = i['name']
        insert_info1['href'] = i['href']
        insert_info1['num'] = i['num']
        db.info.save(insert_info1)
        import_to_mongodb(i['child'], insert_info1['id'])

t = []
t.append(text)
import_to_mongodb(t, 1)

print u'导入成功'
# t.write(str(result))