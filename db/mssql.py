#!/usr/local/python2.6/bin/python
# -*- coding: utf-8 -*-
#简单的一个连接测试
import sys
import pymssql

#reload(sys)
#sys.setdefaultencoding('utf-8') 
print sys.getdefaultencoding()

reload(sys)
sys.setdefaultencoding('utf-8')

print sys.getdefaultencoding()

conn=pymssql.connect(host=u'192.168.1.51'
	,database='futures'
	,user='sa'
	,password='sa123456.'
	,charset='utf8')

cur=conn.cursor()
cur.execute('SELECT TOP 100 * FROM customer')
for r in cur.fetchall():
    #print '\t'.join(str(v) for v in r).encode('utf-8')#.encode('utf-8')
	s = r[2]
	if isinstance(s, unicode): 
		print u"中文1" 
		print s.decode('utf8') 
	#else: 
		#print "中文2" 
		#print s.decode('utf-8').encode('utf-8')
	#print unicode(s.decode('utf-8').encode('utf-8'), 'gbk')
conn.close()