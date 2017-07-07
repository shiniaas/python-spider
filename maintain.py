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
    
    sql_select = "select * from basic where 表名 = %s and 字段名 = %s;"
    sql_add = "insert into basic values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    for i in info.values:
        table_name = i[2]
        field_name = i[3]
        print table_name, field_name
        #插入数据
        values = (table_name, field_name)
        cursor.execute(sql_select, values)
        
        #数据库中没有该记录，为新增的
        if(len(cursor.fetchall()) == 0):
            insert_info = []
            for j in i:
            if isinstance(j, float) and math.isnan(j):
                insert_info.append('')
            else:
                insert_info.append(j)
            #插入数据
            cursor.execute(sql_add, insert_info)
        else:
            
        
        
    #关闭连接
    cursor.execute('commit;')
    connection.close()