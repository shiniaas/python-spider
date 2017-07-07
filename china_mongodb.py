#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client['china']
f = open('t.txt', 'r')
text = eval(f.read())
cur_id = 1


def import_to_mongodb(data, parentid):
    global cur_id
    for i in data:
        insert_info1 = {}
        insert_info1['id'] = cur_id
        cur_id += 1
        insert_info1['parentid'] = parentid
        insert_info1['name'] = i['name']
        insert_info1['href'] = i['href']
        insert_info1['num'] = i['num']
        db.info.save(insert_info1)
        import_to_mongodb(i['child'], insert_info1['id'])

t = []
t.append(text)
import_to_mongodb(t, cur_id)

print u'导入成功'