#!/usr/bin/python2.7 
# -*- coding: utf-8 -*- 
import requests
import json
import urllib,urllib2,httplib
import hashlib
import sys,time,random
import urllib
import urllib2
import cookielib

TOKEN_VERSION='v2'
accessKey = 'AK'
expireTime = int(time.time())+3

headers={'UserAgent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)', 'Content-Type': 'application/json'}
SK = 'B548EC106017EFB2429B7528E65055E5'
#post方式时候要发送的数据
queue = [{"queuenum":"Q01","queuetype":1},
		{"queuenum":"Q02","queuetype":0},
		{"queuenum":"Q03","queuetype":2},
		{"queuenum":"Q04","queuetype":1},
		{"queuenum":"Q05","queuetype":0},
		{"queuenum":"Q06","queuetype":2},
		{"queuenum":"Q07","queuetype":1},
		{"queuenum":"Q08","queuetype":0},
		{"queuenum":"Q09","queuetype":2},
		{"queuenum":"Q10","queuetype":1}]

param = [{"hallno":'1',"bizlist":["1","2","XC01","XC02","XC03","XC04","DL02","DL03","DL04","DL05","DL07","DL08","DL09","DL10","DL22","XC05","DL01","DL06","DL11","DL12","DL13","DL14","DL15","DL16","DL17","DL18","DL19","DL20","DL21","DL23","DL24","XC06","XC07","XC08","XC09","XC10"],"counterlist":["1","2","3"],"elist":["10001","10002"]},
		{"hallno":'A001',"bizlist":["001","003","350200-XM-021","002","1"],"counterlist":["HALL-TEST1-#1","HALL-TEST2-#3","C01","C03"],"elist":["1","2","3","4","5","6","7","0001","8","9"]},
		{"hallno":'A002',"bizlist":["004","350200-XM-022"],"counterlist":["1HALL-TEST2-#1","HALL-TEST2-#2","5","C04","C05","C051"],"elist":["21","22","23"]}]
inte = 'http://localhost:8080/sysqueueinterface'
url_ = "http://localhost:8080/gethalldata.action"
opener_ = urllib2.build_opener()
opener_.addheaders.append(('Cookie', 'user.cookie="admin,123456,    (    )"'))
r_ = opener_.open(url_)

param = json.loads(json.loads(r_.read()))
r_.close()
opener_.close()
	
a1=(2018,10, 16, 0,0,0,0,0,0)
a2=(2018,10, 31, 23,59,59,0,0,0) 
start=time.mktime(a1)    #生成开始时间戳
end=time.mktime(a2)      #生成结束时间戳

while start<end:
	s = time.localtime(start)
	start = start + 24 * 60 * 60
	for hall in param:
		elist = hall["elist"]
		hallno = hall["hallno"]
		counterlist = hall["counterlist"]
		print elist, hallno, counterlist
		for i in range(0, len(elist)):
			eid = elist[i]
			if i<len(counterlist):
				counterid = counterlist[i]
			else:
				counterid = ""
					

			print "员工ID:" + eid + ",窗口：" + counterid + ", 时间: " + time.strftime("%Y-%m-%d %H:%M:%S", s)
			if counterid == "":
				continue
			
			###########################################登录
			t1=random.randint(start - 24 * 60 * 60, start)
			#print '随机：' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start - 24 * 60 * 60))  + "...." + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start))
			t = time.localtime(t1)
			localtime = time.strftime("%Y-%m-%d %H:%M:%S", t)
			tt=time.strftime("%Y%m%d%H%M%S", t) 
			data = '%s%s'%(tt, SK)
			print 'token数据：' + data
			
			hash_md5 = hashlib.md5(data)
			s2 = hash_md5.hexdigest()
			values={"service":"login","account":"ACCOUNT","password":s2,"hallno":hallno,"counterno":counterid,"serverno":eid,"servername":"","eventtime":localtime,"tt":tt}
			request=urllib2.Request(inte, headers=headers)
			data = json.dumps(values) # , ensure_ascii=False
			#获得回送的数据
			response=urllib2.urlopen(request, data)
			#print data
			
			###########################################

			###########################################退出
			waittime = random.randint(3600*1, 3600*3)
			t = time.localtime(t1+waittime)
			localtime = time.strftime("%Y-%m-%d %H:%M:%S", t) 
			tt=time.strftime("%Y%m%d%H%M%S", t) 
			data = '%s%s'%(tt, SK)
			hash_md5 = hashlib.md5(data)
			s2 = hash_md5.hexdigest()
			values={"service":"unlogin","account":"ACCOUNT","password":s2,"hallno":hallno, "counterno":counterid,"eventtime":localtime,"tt":tt}
			request=urllib2.Request(inte, headers=headers)
			data = json.dumps(values) # , ensure_ascii=False
			#获得回送的数据
			response=urllib2.urlopen(request, data)
			#print data
			###########################################
		
	