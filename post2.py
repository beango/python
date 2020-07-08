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
reload(sys)
sys.setdefaultencoding('utf8')

TOKEN_VERSION='v2'
accessKey = 'AK'
expireTime = int(time.time())+3

headers={'UserAgent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)', 'Content-Type': 'application/json'};
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
inte = 'http://localhost:8081/sysqueueinterface'
url_ = "http://localhost:8081/gethalldata.action"
opener_ = urllib2.build_opener()
opener_.addheaders.append(('Cookie', 'user.cookie="admin,123456,    (    )"'))
r_ = opener_.open(url_)

param = json.loads(json.loads(r_.read()))
r_.close()
opener_.close()
a=100
while a>0:
	a -= 1
	queueobj = queue[random.randint(0, len(queue)-1)]
	queuenum = queueobj["queuenum"]
	queuetype = queueobj["queuetype"]
	#print queuenum, queuetype

	d1 = param[random.randint(0, len(param)-1)]
	#print json.dumps(d1)
	hallno = d1["hallno"]
	bizlist = d1["bizlist"]
	bizid = bizlist[random.randint(0, len(bizlist)-1)]
	counterlist = d1["counterlist"]
	counterid = counterlist[random.randint(0, len(counterlist)-1)]
	elist = d1["elist"]
	eid = elist[random.randint(0, len(elist)-1)]
	
	###########################################登录
	curtime = time.localtime(time.time())
	localtime = time.strftime("%Y-%m-%d %H:%M:%S", curtime) 
	tt=time.strftime("%Y%m%d%H%M%S", time.localtime()) 
	data = '%s%s'%(tt, SK)
	print 'token数据：' + data
	hash_md5 = hashlib.md5(data)
	s2 = hash_md5.hexdigest()
	values={"service":"login","account":"ACCOUNT","password":s2,"hallno":hallno,"counterno":counterid,"serverno":eid,"servername":"","eventtime":localtime,"tt":tt}
	request=urllib2.Request(inte, headers=headers);
	data = json.dumps(values) # , ensure_ascii=False
	#获得回送的数据
	response=urllib2.urlopen(request, data);
	#print data
	
	###########################################

	###########################################退出
	waittime = random.randint(3600*1, 3600*3)
	curtime = time.localtime(time.time()+waittime)
	localtime = time.strftime("%Y-%m-%d %H:%M:%S", curtime) 
	tt=time.strftime("%Y%m%d%H%M%S", time.localtime()) 
	data = '%s%s'%(tt, SK)
	print 'token数据：' + data
	hash_md5 = hashlib.md5(data)
	s2 = hash_md5.hexdigest()
	values={"service":"unlogin","account":"ACCOUNT","password":s2,"hallno":hallno, "counterno":counterid,"eventtime":localtime,"tt":tt}
	request=urllib2.Request(inte, headers=headers);
	data = json.dumps(values) # , ensure_ascii=False
	#获得回送的数据
	response=urllib2.urlopen(request, data);
	#print data
	###########################################
	
	###########################################暂停
	waittime = 0
	curtime = time.localtime(time.time()+waittime)
	localtime = time.strftime("%Y-%m-%d %H:%M:%S", curtime) 
	tt=time.strftime("%Y%m%d%H%M%S", time.localtime()) 
	data = '%s%s'%(tt, SK)
	print 'token数据：' + data
	hash_md5 = hashlib.md5(data)
	s2 = hash_md5.hexdigest()
	values={"service":"pause","account":"ACCOUNT","password":s2,"hallno":hallno,"counterno":counterid, "eventtime":localtime,"tt":tt}
	request=urllib2.Request(inte, headers=headers);
	data = json.dumps(values) # , ensure_ascii=False
	#获得回送的数据
	response=urllib2.urlopen(request, data);
	#print data
	###########################################

	###########################################取消暂停
	waittime = random.randint(600, 1200)
	curtime = time.localtime(time.time()+waittime)
	localtime = time.strftime("%Y-%m-%d %H:%M:%S", curtime) 
	tt=time.strftime("%Y%m%d%H%M%S", time.localtime()) 
	data = '%s%s'%(tt, SK)
	print 'token数据：' + data
	hash_md5 = hashlib.md5(data)
	s2 = hash_md5.hexdigest()
	values={"service":"cancelpause","account":"ACCOUNT","password":s2,"hallno":hallno,"counterno":counterid,"eventtime":localtime,"tt":tt}
	request=urllib2.Request(inte, headers=headers);
	data = json.dumps(values) # , ensure_ascii=False
	#获得回送的数据
	response=urllib2.urlopen(request, data);
	#print data
	###########################################
