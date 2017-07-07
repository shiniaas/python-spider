#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json
import xlwt
import time
import random
from pymongo import MongoClient

proxy_list = [{'http' : 'xxx'}, {'http' : 'xxx'}, {'http' : 'xxx'}, {'http' : 'xxx'}]


header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
            'Accept': 'ttext/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
         }

    
url0 = 'http://d.qianzhan.com'

t = open('china2.txt', 'w')

result = {'url':'', 'class':'', 'detailed':[]}


def get_proxy():
    global proxy_list
    index = random.randint(0, len(proxy_list)-1)
    return proxy_list[index]

def get_detailed_info(url):
    result['url'] = url
    t = {'name':'',  'unit':'', 'time':'', 'href':''}
    
    proxy = get_proxy()
    text = requests.get(url, headers = header, proxies = proxy).text
    html = BeautifulSoup(text, 'lxml')
    result['class'] = html.find('div', attrs={'class':'search-result-tit'}).find('em').get_text()
    
    flag0 = 1
    while flag0:
        cnt = 5
        flag = 0
        while cnt > 0 and flag == 0:
            try:
                proxy = get_proxy()
                text = requests.get(url, headers = header, proxies = proxy).text
                html = BeautifulSoup(text, 'lxml')
                con = html.find('table', attrs={'class':'search-result_table search-result_table2 '}).find('tbody').find_all('tr')
                del(con[0])
                for i in con:
                    content = i.find_all('td')
                    t['name'] = content[0].get_text()
                    t['unit'] = content[1].get_text()
                    t['time'] = content[2].get_text()
                    href = url0 + content[3].find_all('a')[1].get('href')
                    t['href'] = href
                    result['detailed'].append(t)
                url1 = html.find('div', attrs = {'class':'listpage'}).find_all('a')[-1].get('href')
                if not url1:
                    print 'over'
                    flag0 = 0
                    break
                url = url0 + url1
            except:
                time.sleep(1)
                cnt -= 1
            
        
get_detailed_info('http://d.qianzhan.com/xdata/list/xCxrxixWxW.html')    
print len(result['detailed'])

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client['china']

db.detailed.save(result)

#t.write(str(result))
        