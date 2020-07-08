#!/usr/bin/python
#coding=utf-8
 
import urllib,urllib2
import random 
import time
import datetime

uri = 'http://192.168.1.199:8083/queueSysinterface.aspx'

i = 1
count = random.randint(150, 170)
t = datetime.datetime.strptime("2018-07-02 8:40:00", "%Y-%m-%d %H:%M:%S")
count = 0
if i<=1:
	params = "{\"interfacename\":\"getserverinfo\",\"serverno\":\"1\"}" # urllib.urlencode(params)
	req = urllib2.Request(uri, params)    #生成页面请求的完整数据
	response = urllib2.urlopen(req)     #发送页面请求
	print response.read()    #获取服务器返回的页面信息
	# print '               ' + params
	time.sleep(0.01)

	count += 1
	i+=1
	
print "总收到%d条结果"%count



params = "{\"interfacename\":\"getcounterinfo\",\"counterno\":\"1\"}" # urllib.urlencode(params)
req = urllib2.Request(uri, params)    #生成页面请求的完整数据
response = urllib2.urlopen(req)     #发送页面请求
print response.read()    #获取服务器返回的页面信息