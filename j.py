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
insert_info = []
insert_info.append(cur_id)
insert_info.append(cur_id)
cur_id += 1
insert_info.append(text['name'])
insert_info.append(text['href'])
insert_info.append(text['num'])

cursor.execute(sql_add, insert_info)

for i in text['child']:
    insert_info1 = []
    insert_info1.append(cur_id)
    cur_id += 1
    insert_info1.append(insert_info[0])
    insert_info1.append(i['name'])
    insert_info1.append(i['href'])
    insert_info1.append(i['num'])
    cursor.execute(sql_add, insert_info1)
    for j in i['child']:
        insert_info2 = []
        insert_info2.append(cur_id)
        cur_id += 1
        insert_info2.append(insert_info1[0])
        insert_info2.append(j['name'])
        insert_info2.append(j['href'])
        insert_info2.append(j['num'])
        cursor.execute(sql_add, insert_info2)

cursor.execute('commit;')
connection.close()