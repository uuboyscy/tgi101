# 連接資料庫
import pymysql

host = 'localhost'
port = 3306
user = 'root'
passwd = 'root'
db = 'TESTDB'
charset = 'utf8mb4'

conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
print('Successfully connected!')

cursor = conn.cursor()

import json
import time

path = 'Staff.json'
with open(path, 'r', encoding='utf-8') as f:
    jsondata = json.loads(f.read())

# 先寫好 SQL 語法
# 並將語法中會不斷改變的部分挖空 ( %s )
sql_insert = """
INSERT INTO Staff (ID, Name, DeptId, Age, Gender, Salary, recordDt)
VALUES (%s, %s, %s, %s, %s, %s, %s);
"""

# 整理 jsondata 成可 insert 進資料庫的樣子，格式如下
'''
[('001', 'Mike', '002', '45', 'M', '60000', '2020-10-13 21:41:49'),
 ('002', 'Judy', '002', '30', 'F', '48000', '2020-10-13 21:41:49'),
 ('003', 'Allen', '001', '22', 'M', '50000', '2020-10-13 21:41:49'),
 ('004', 'Tom', '002', '47', 'M', '47000', '2020-10-13 21:41:49'),
 ('005', 'Jack', '003', '36', 'M', '52000', '2020-10-13 21:41:49'),
 ('006', 'Abby', '002', '24', 'F', '45000', '2020-10-13 21:41:49'),
 ('007', 'Trump', '001', '80', 'M', '80000', '2020-10-13 21:41:49'),
 ('008', 'Marry', '003', '29', 'F', '87000', '2020-10-13 21:41:49')]
'''
import time
t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
values = [tuple(jsondata[d].values()) + (t,) for d in jsondata]

print('新增資料筆數:', cursor.executemany(sql_insert, values))

# Commit 並檢查資料是否存入資料庫
conn.commit()

# 關閉連線
cursor.close()
conn.close()