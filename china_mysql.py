#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql.cursors
f = open('t.txt', 'r')
text = eval(f.read())

#将数据导入到mysql，给每一条记录一个id

#连接数据库
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

sql_add = "insert into china(id, parentid, name, href, num) values(%s, %s, %s, %s, %s);"
cur_id = 1

#将最高节点的id和parent_id设置为一样

def import_to_mysql(data, parentid):
    global cur_id
    for i in data:
        insert_info1 = []
        insert_info1.append(cur_id)
        cur_id += 1
        insert_info1.append(parentid)
        insert_info1.append(i['name'])
        insert_info1.append(i['href'])
        insert_info1.append(i['num'])
        cursor.execute(sql_add, insert_info1)
        import_to_mysql(i['child'], insert_info1[0])

t = []
t.append(text)
import_to_mysql(t, cur_id)
cursor.execute('commit;')
connection.close()