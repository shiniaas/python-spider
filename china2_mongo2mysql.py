#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pymongo import MongoClient
import pymysql.cursors

def import_to_mysql(href):

    connection = pymysql.connect(host = 'localhost',
                         port = 3306,
                         user = 'root',
                         password = '123456',
                         charset = 'utf8'
                         )
    cursor = connection.cursor()

    #进入数据库
    sql = 'use lifan;'
    cursor.execute(sql)
    
    sql_insp = 'insert into detailed_parent(href, class) values(%s, %s);'
    sql_insc = 'insert into detailed_child(parent_id, href, name, unit, time) values(%s, %s, %s, %s, %s);'
    
    client = MongoClient('localhost', 27017)
    db = client['china']
    t = db.detailed.find({}, {'url':href, 'class':'', 'detailed':''})
    for i in t:
        l_mysql = []
        l_mysql.append(i['url'])
        l_mysql.append(i['class'])
        cursor.execute(sql_insp, l_mysql)
        cursor.execute('commit')
        cursor.execute('select id from detailed_parent where href = %s', (href, ))
        num = cursor.fetchone()[0]
        
        for j in i['detailed']:
            l_mon = []
            l_mon.append(num)
            l_mon.append(j['href'])
            l_mon.append(j['name'])
            l_mon.append(j['unit'])
            l_mon.append(j['time'])
            cursor.execute(sql_insc, l_mon)
            cursor.execute('commit')

import_to_mysql('http://d.qianzhan.com/xdata/list/xCxrxixWxW.html')
print 'over'