#!/usr/bin/python
#coding=utf-8
 
import urllib,urllib2
import random 
import time
import datetime

uri = 'http://192.168.1.199:8083/queueSysinterface.aspx'
uri = "http://111.230.14.84:8088/queueSysinterface.aspx"
uri = "http://localhost:8080/queuectl"
i = 1
count = random.randint(150, 170)
t = datetime.datetime.strptime("2018-07-02 8:40:00", "%Y-%m-%d %H:%M:%S")
count = 0;
if i<=50000:
	params = "{\"interfacename\":\"getserverinfo\",\"serverno\":\"1\"}" # urllib.urlencode(params)
	req = urllib2.Request(uri, params)    #生成页面请求的完整数据
	#response = urllib2.urlopen(req)     #发送页面请求
	#print response.read()    #获取服务器返回的页面信息
	time.sleep(0.01)

	count += 1
	i+=1
	
print "总收到%d条结果"%count




def getcounterwaitpersons():
	params = "{\"interfacename\":\"getcounterwaitpersons\",\"counterno\":\"1\"}" # urllib.urlencode(params)
	req = urllib2.Request(uri, params)    #生成页面请求的完整数据
	response = urllib2.urlopen(req)     #发送页面请求
	print response.read()    #获取服务器返回的页面信息

def counterlogin():
	# 窗口登录接口
	params = "{\"interfacename\":\"counterlogin\",\"counterno\":\"1\",\"staffid\":\"1\",\"password\":\"\"}"
	req = urllib2.Request(uri, params)
	response = urllib2.urlopen(req)
	print response.read()

def counterlogin2():
	# 签退接口
	params = "{\"interfacename\":\"counterunlogin\",\"counterno\":\"1\"}"
	req = urllib2.Request(uri, params)
	response = urllib2.urlopen(req)
	print response.read()


	# 获取下一位排队号码接口
	params = "{\"interfacename\":\"getnextnumber\",\"counterno\":\"1\"}"
	req = urllib2.Request(uri, params)
	response = urllib2.urlopen(req)
	print response.read()

	# 获取等候人数接口
	params = "{\"interfacename\":\"getcounterwaitpersons\",\"counterno\":\"1\"}"
	req = urllib2.Request(uri, params)
	response = urllib2.urlopen(req)
	print response.read()

	# 窗口事件触发接口
	params = "{\"interfacename\":\"countereventaction\",\"counterno\":\"1\",\"staffid\":\"1\",\"serialid\":\"1\",\"transcodeid\":\"20160315092000-0001-A001\",\"eventid\":\"1\",\"number\":\"A001\"}"
	req = urllib2.Request(uri, params)
	response = urllib2.urlopen(req)
	print response.read()

	# 排队号转移
	params = "{\"interfacename\":\"countertransfer\",\"counterno\":\"1\",\"transfertype\":\"1\",\"transcodeid\":\"20160315092000-0001-A001\",\"transfervalue\":\"1\",\"number\":\"A001\"}"
	req = urllib2.Request(uri, params)
	response = urllib2.urlopen(req)
	print response.read()

counterlogin();