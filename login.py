#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json
import xlwt
import time
import random
import threading
import Queue
from pymongo import MongoClient

RES = []

thread_id = 1
THREAD_NUM = 2

class qianzhan(threading.Thread):
    def __init__(self, queue):
        global thread_id
        threading.Thread.__init__(self)
        self.queue = queue
        self.thread_id = thread_id
        thread_id += 1
        

    def run(self):
        while True:
            try:
                task = self.queue.get(block = True, timeout = 1) #如果不设timout会阻塞
            except Queue.Empty:
                break 
            #运行程序
            print 'task' , self.thread_id, 'begin'
            r = get_info(task[0], task[1])
            print r
            global RES
            RES.append(r)
            self.queue.task_done()
            print 'task' , self.thread_id, 'end'

def get_info(url, account):
    cnt = 5
    flag = 0
    while cnt > 0 and flag == 0:
        try:
            header = {
                        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Accept-Encoding': 'gzip, deflate',
                        'Connection': 'keep-alive'
                     }
            
            session = requests.Session()
            proxy = {'http' : 'xxx'}

            url_login = 'http://user.qianzhan.com/account/doLogin?username=' + account['user'] + '&userpwd=' + account['password']

            #登录
            text = session.get(url_login, headers = header, proxies = proxy)

            text = session.get(url, headers = header, proxies = proxy).content

            html = BeautifulSoup(text, 'lxml')
            
            result = {'url':url, 'data':[]}
            
            t_list = html.find('table', attrs = {'class': 'search-result_table'}).find('tbody').find_all('tr')
            del(t_list[0])
            del(t_list[0])
            for i in t_list:
                con = {'time':'', 'value':''}
                t = i.find_all('td')
                con['time'] = t[1].get_text()
                con['value'] = t[2].get_text()
                result['data'].append(con)
            return result
            flag = 1
        except:
            cnt -= 1
            print 'fail' + url
    

def import_to_mongodb(data):
    client = MongoClient('localhost', 27017)
    db = client['china']
    for i in data:
        print len(i['data'])
        db.task3.save(i)
    print 'import to mongodb success'
    
if __name__ == '__main__':
    account = {
                'user':'',
                'password':''
              }
    user = raw_input('user:')
    password = raw_input('password:')
    account['user'] = user
    account['password'] = password
    url_list = ['http://d.qianzhan.com/xdata/details/1d73c3541b696502.html', 'http://d.qianzhan.com/xdata/details/b2f281ab55a6af5a.html']
    q = Queue.Queue(10)
    
    for i in range(0, THREAD_NUM):
        worker = qianzhan(q)
        worker.start()
    for i in url_list:
        q.put([i, account], block = True)
    q.join()
    
    import_to_mongodb(RES)