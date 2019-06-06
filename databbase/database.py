import pymysql

db = pymysql.connect(host='140.116.163.9',
                     port=10002,
                     user='dltlab',
                     password='dltlab@nckucs',
                     db='epslab_ems',
                     charset='utf8')

cursor = db.cursor()

sql = 'SELECT VERSION()'

cursor.execute(sql)

data = cursor.fetchone()

print("Database version : %s " % data)

db.close()
