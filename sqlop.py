import sqlite3 as sl

while(1):
    sql = input(">>>")
    con = sl.connect('menbers.db')
    cursor = con.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    print(type(data))
    print(data)
    con.commit()
    con.close()