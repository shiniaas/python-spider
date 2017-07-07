 #!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql.cursors
import xlwt
import time

f = xlwt.Workbook()
sheet1 = f.add_sheet('sheet1', cell_overwrite_ok=True)

sql_first = 'select * from china where parentid = id';
sql_sel = 'select * from china where parentid != id and parentid = %s'

# 连接数据库
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

cur_row = 0
def write_excel(parentid, level):
    #输出最高级的所有子节点
    global cur_row
    data = []
    if parentid == 0:
        cursor.execute(sql_first)
        data = cursor.fetchall()
    else:
        cursor.execute(sql_sel, (parentid, ))
        data = cursor.fetchall()
    if len(data) == 0:
        return
    #说明有数据
    for i in data:
        column = level
        for j in i:
            sheet1.write(cur_row, column, j)
            column += 1
        cur_row += 1
        return write_excel(i[0], level+1)
        
        
write_excel(0, 0)
connection.close()
f.save('china.xls')
