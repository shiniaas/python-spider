#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql.cursors
import pandas as pd
import math

#第一次导入数据
if __name__ == '__main__':
    #读取excel表格
    info = pd.read_excel('import_to_mysql.xlsx')
    
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
    
    sql = "insert into basic values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    for i in info.values:
        insert_info = []
        #去掉nan
        for j in i:
            if isinstance(j, float) and math.isnan(j):
                insert_info.append('')
            else:
                insert_info.append(j)
        #插入数据
        cursor.execute(sql, insert_info)
        
    #关闭连接
    cursor.execute('commit;')
    connection.close()