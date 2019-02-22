#!/usr/bin/python
#coding=utf-8
 
import urllib,urllib2
import random 
import time
import datetime

uri = 'http://111.230.14.84:8080/appriesAddDebug'
idcard = ['2','3','14','111','10010','10011','8888','1']
mac = ['0800274CF9F1',
'080027ED1CE8',
'08002728F280',
'080027DF75A9',
'080027BF10D0',
'0800275DFB23',
'080027F9A397',
'983B16523D70'
,'442C05AE8FE5' # 7测试设备
,'CCB8A8DB14F8'  # 10寸
]

i = 1
count = random.randint(180, 220)
t = datetime.datetime.strptime("2018-06-30 8:40:00", "%Y-%m-%d %H:%M:%S")
while i<=count:
	r = random.randint(100, 200)
	t = t + datetime.timedelta(seconds = r)
	#print t
	params = {};
	params['appriesDate'] = t.strftime("%Y-%m-%d %H:%M:%S")
	params['mac'] = mac[random.randint(0, len(mac)-1)]
	params['cardNum'] = idcard[random.randint(0, len(idcard)-1)]
	params['appriesButton'] = random.randint(0, 6)
	params['bussinessTime'] = r
	params['idCard'] = ''
	params['tel'] = ''
	params = urllib.urlencode(params)
	req = urllib2.Request(uri, params)    #生成页面请求的完整数据
	response = urllib2.urlopen(req)     #发送页面请求
	#print response.read()    #获取服务器返回的页面信息
	#print '               ' + params
	i+=1



