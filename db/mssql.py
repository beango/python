#-*-encoding:utf-8-*-
 
#简单的一个连接测试
import pymssql
conn=pymssql.connect(host='192.168.1.51'
	,database='futures'
	,user='sa'
	,password='sa123456.'
	,charset="UTF-8")
cur=conn.cursor()
cur.execute('SELECT TOP 100 * FROM customer')
for r in cur.fetchall():
    #print '\t'.join(str(v) for v in r).encode('utf-8')#.encode('utf-8')
    print r[2].encode('utf-8')
conn.close()