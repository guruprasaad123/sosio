import mysql.connector
import csv

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

rows =[['sin','insertion_datetime','datetime','open','high','low','close','volume','open_interest']]

for i,c in enumerate(results):
    (isin,insertion_datetime,datetime,open_,high,low,close,volume,open_interest) = c
    #(date , time) = str(datetime).split(' ')
    if(i%1000 == 0):
        print('written {} rows'.format(i))
    rows.append([isin,insertion_datetime,datetime,open_,high,low,close,volume,open_interest])


with open('stocks_1.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(rows)

csvfile.close()

print(conn)