import mysql.connector

'''pip install mysql-connector-python'''
conn = mysql.connector.connect(
         user='foouser',
         password='F88Pa%%**',
         host='134.209.144.239',
         database='stocksdb')
cursor = conn.cursor()
#'SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME="interview"'
cursor.execute('SELECT * FROM interview')

results = cursor.fetchall()


for c in results:
    (isin,insertion_datetime,datetime,open_,high,low,close,volume,open_interest) = c
    print('isin',isin)
    print('insertion_datetime',insertion_datetime)
    print('datetime',datetime)
    print('open',open_)
    print('high',high)
    print('low',low)
    print('close',close)
    print('volume',volume)
    print('open_interest',open_interest)
    break;
    
print(conn)