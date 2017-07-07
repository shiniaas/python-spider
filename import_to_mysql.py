#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql.cursors
import xlrd
import xlwt

def insert_new():
    book = xlrd.open_workbook("import_to_mysql.xlsx")
    sheet = book.sheet_by_name("Sheet1")
    
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
    
    sql_add = "insert into basic values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    for i in range(1, sheet.nrows):
        insert_info = []
        for j in range(0, 11):
            insert_info.append(str(sheet.cell(i, j).value))
        cursor.execute(sql_add, insert_info)
        
    #关闭连接
    cursor.execute('commit;')
    connection.close()
    
def maintain_excel():
    book = xlrd.open_workbook("import_to_mysql.xlsx")
    sheet = book.sheet_by_name("Sheet1")
    keyword = []
    for i in range(1, sheet.nrows):
        t_list = []
        t_list.append(sheet.cell(i, 2).value)
        t_list.append(sheet.cell(i, 3).value)
        keyword.append(t_list)

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
    
    sql_delete = "delete from basic where 表名 = %s and 字段名 = %s;"
    sql_select = "select * from basic where 表名 = %s and 字段名 = %s;"
    sql_add = "insert into basic values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    #先找数据库中是否有多余的数据
    sql = "select * from basic"
    cursor.execute(sql)
    for i in cursor.fetchall():
        t_list = []
        t_list.append(i[2])
        t_list.append(i[3])
        if t_list not in keyword:
            #需要删除
            cursor.execute(sql_delete, t_list)
            cursor.execute("commit;")
    
    #遍历excel表格，增加和修改
    for i in range(1, sheet.nrows):
        t_list = []
        t_list.append(str(sheet.cell(i, 2).value))
        t_list.append(str(sheet.cell(i, 3).value))
        cursor.execute(sql_select, t_list)
        data = cursor.fetchall()
        if len(data) == 0:
            #表明是新增加的元组
            insert_info = []
            for j in range(0, 11):
                insert_info.append(str(sheet.cell(i, j).value))
            cursor.execute(sql_add, insert_info)
            cursor.execute("commit;")
        else:
            #检测修改
            info_excel = []
            for j in range(0, 11):
                info_excel.append(sheet.cell(i, j).value)
            info_sql = data[0]
            flag = 0
            for k in range(0, 11):
                if info_excel[k] != info_sql[k]:
                    flag = 1
                    break
            if flag == 1:
                sql = sql_delete + sql_add
                t_list = []
                t_list.append(info_excel[2])
                t_list.append(info_excel[3])
                for l in info_excel:
                    t_list.append(l)
                cursor.execute(sql, t_list)
                cursor.execute("commit")
    connection.close()


if __name__ == '__main__':
    #insert_new()
    maintain_excel()