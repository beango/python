#coding=gbk  
import httplib  
conn = httplib.HTTPConnection("localhost:12345")  
conn.request('get', '/123.html')  
print conn.getresponse().read()  
conn.close() 
