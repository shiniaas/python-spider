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
t = open('t.txt', 'w')

#获取中国宏观下的所有指标
text = requests.get(url0 + url1, headers = header, proxies = proxy).text
html = BeautifulSoup(text, 'lxml')

#保存中国宏观的数量
num = html.find('div', attrs = {'class':'search-result-tit'}).find_all('em')[2].get_text()
result['num'] = num

#获取中国宏观的所有孩子
child_all = html.find('div', attrs = {'class':'searchfilter_sub'}).find_all('a')

#删除第一个即全部
del(child_all[0])
#将中国宏观下的内容保存到child中
for i in child_all:
    name = i.get_text()
    href = i.get('href')
    t_dict = {'name':'', 'href':'', 'child':[], 'num':''}
    t_dict['name'] = name
    t_dict['href'] = url0 + href
    result['child'].append(t_dict)

#爬取一级的孩子
for i in result['child']:
    cnt = 5
    flag = 0
    while cnt > 0 and flag == 0:
        try:        
            text = requests.get(i['href'], headers = header, proxies = proxy).text
            html = BeautifulSoup(text, 'lxml')

            #保存一级孩子的数量
            print i['href']
            num = html.find('div', attrs = {'class':'search-result-tit'}).find_all('em')[2].get_text()
            i['num'] = num

            # print html
            child_all = html.find_all('div', attrs = {'class':'searchfilter_sub'})[1].find_all('a')
            # 删除第一个即全部
            del(child_all[0])
            # 将一级孩子下的内容保存到child中
            for j in child_all:
                name = j.get_text()
                href = j.get('href')
                t_dict = {'name':'', 'href':'', 'child':[], 'num':''}
                t_dict['name'] = name
                t_dict['href'] = url0 + href
                i['child'].append(t_dict)
            print 'success'
            flag = 1
        except:
            time.sleep(1)
            cnt -= 1
            continue
    if flag == 0:
        print 'fail'
# 爬取二级的数量

for i in result['child']:
    # 将一级孩子下的内容保存到child中
    for j in i['child']:
        cnt = 5
        flag = 0
        while cnt > 0 and flag == 0:
            try:
                text = requests.get(j['href'], headers = header, proxies = proxy).text
                html = BeautifulSoup(text, 'lxml')
                print j['href']
                # 保存一级孩子的数量
                num = html.find('div', attrs = {'class':'search-result-tit'}).find_all('em')[2].get_text()
                j['num'] = num
                print 'success'
                flag = 1
                cnt = cnt - 1
            except:
                time.sleep(1)
                cnt -= 1
                continue
        if flag == 0:
            print 'fail'

#保存结果            
t.write(str(result))