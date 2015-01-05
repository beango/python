#!/usr/local/python2.6/bin/python
# -*- coding: utf-8 -*-
#简单的一个连接测试
import sys,os
import pymssql
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

reload(sys)
sys.setdefaultencoding('utf-8') 

import cx_Oracle

#建立和数据库系统的连接  
conn = cx_Oracle.connect('dev/sa123456.@192.168.4.92/orcl')  
#获取操作游标  
cursor = conn.cursor()  
cursor.execute("select pkid,交易商代码,importtime from IMPORTPOSITIONS where rownum<=10")  
#获取一条记录  
one = cursor.fetchone()  
print '1: id:%d,交易商代码:%s,,importtime:%s'%one;
#获取两条记录!!!注意游标已经到了第二条    
two = cursor.fetchmany(2)   
print '2 and 3:',two[0],two[1]     
#获取其余记录!!!注意游标已经到了第四条  
three = cursor.fetchall();   
#for row in three:    
#	print row   #打印所有结果    
print 'find'  
cursor.prepare(u"""select count(*) from T_IMPORTPOSITIONS where 交易商代码 = :id""")  
cursor.execute(None,{'id':'045400413'})    
for row in cursor:  #相当于fetchall()  
	print row[0]
cursor.close();  
conn.close();  