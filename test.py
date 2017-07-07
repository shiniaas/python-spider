import pymysql.cursors

connection = pymysql.connect(host = 'localhost',
                             port = 3306,
                             user = 'root',
                             password = '123456',
                             charset = 'utf8'
                             )

try:
    with connection.cursor() as cursor:
        sql = 'use lifan;'
        cursor.execute(sql)
        sql = 'select name from info;'
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result[0])
finally:
    connection.close()