#!/usr/bin/python2.7 
# -*- coding: utf-8 -*- 
import requests
import json
import urllib,urllib2,httplib
import hashlib
import sys,time,random
from datetime import datetime 
import urllib2
import cookielib
reload(sys)
sys.setdefaultencoding('utf8')

TOKEN_VERSION='v2'
accessKey = 'AK'
inte = 'http://localhost:8081/sysqueueinterface'
intedata = "http://localhost:8081/gethalldata.action"
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


opener = urllib2.build_opener()
opener.addheaders.append(('Cookie', 'user.cookie="admin,123456,    (    )"'))
r = opener.open(intedata)
param = json.loads(json.loads(r.read()))
r.close()
opener.close()

counts = 1000 #执行次数2018-09-29 14:56:40.000
ticks = (datetime.now() - datetime.strptime('2018-08-02 8:56:59.000',"%Y-%m-%d %H:%M:%S.%f")).total_seconds() * -1 #生成N秒前的数据

while counts>0:
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
	
	#print hallno, bizid, counterid, eid
	
	t = time.localtime(time.time() + ticks)
	localtime = time.strftime("%Y-%m-%d %H:%M:%S", t) 
	ywlsh=time.strftime("%Y%m%d%H%M%S", t) 
	#ywlsh=20180924101743
	tt = ywlsh

	###########################################取号
	data = '%s%s'%(ywlsh, SK)
	print 'token数据：' + data
	hash_md5 = hashlib.md5(data)
	s2 = hash_md5.hexdigest()
	values={"account":"ACCOUNT","password":s2,"service":"addticketrecord","hallno":hallno,"bizid":bizid,"cardid":"350583198911304369","cardname":u"张三","cardtype":u"身份证","queuenum":queuenum,"queuetype":queuetype,"ywlsh":ywlsh,"eventtime":localtime,"tt":tt,"isproxy":random.randint(0,1)}
	request=urllib2.Request(inte, headers=headers);
	data = json.dumps(values) # , ensure_ascii=False
	#获得回送的数据
	response=urllib2.urlopen(request, data);
	#print data
	#continue
	###########################################
	
	###########################################叫号
	waittime = random.randint(100, 200)
	t = time.localtime(time.time() + ticks + waittime)
	localtime = time.strftime("%Y-%m-%d %H:%M:%S", t) 
	tt=time.strftime("%Y%m%d%H%M%S", t) 
	data = '%s%s'%(tt, SK)
	hash_md5 = hashlib.md5(data)
	s2 = hash_md5.hexdigest()
	isabort = random.randint(1, 15)!=1
	if isabort:
		values={"service":"call","account":"ACCOUNT","password":s2,"ywlsh":ywlsh,"hallno":hallno, "bizid":bizid,"queuenum":queuenum,"eventtime":localtime,"userid":eid,"windowno":counterid,"tt":tt}
		request=urllib2.Request(inte, headers=headers);
		data = json.dumps(values, ensure_ascii=False)
		#获得回送的数据
		response=urllib2.urlopen(request, data);
		#print response.read()

		###########################################开始办理
		if random.randint(1, 10)!=1:
			waittime = waittime+random.randint(100, 200)
			t = time.localtime(time.time() + ticks + waittime)
			localtime = time.strftime("%Y-%m-%d %H:%M:%S", t) 
			tt=time.strftime("%Y%m%d%H%M%S", t) 
			data = '%s%s'%(tt, SK)
			hash_md5 = hashlib.md5(data)
			s2 = hash_md5.hexdigest()
			values={"service":"service","account":"ACCOUNT","password":s2,"ywlsh":ywlsh,"hallno":hallno,"bizid":bizid,"queuenum":queuenum,"eventtime":localtime, "servicetype":"1","tt":tt}
			request=urllib2.Request(inte, headers=headers);
			data = json.dumps(values, ensure_ascii=False)
			#获得回送的数据
			response=urllib2.urlopen(request, data);
			#print response.read()
		###########################################

	else:
		print '没有叫号'
	###########################################
	
	

	###########################################结束办理
	if random.randint(1, 10)!=1:
		waittime = waittime+random.randint(100, 200)
		t = time.localtime(time.time() + ticks + waittime)
		localtime = time.strftime("%Y-%m-%d %H:%M:%S", t) 
		tt=time.strftime("%Y%m%d%H%M%S", t) 
		data = '%s%s'%(tt, SK)
		hash_md5 = hashlib.md5(data)
		s2 = hash_md5.hexdigest()
		values={"service":"service","account":"ACCOUNT","password":s2,"ywlsh":ywlsh,"hallno":hallno,"bizid":bizid,"queuenum":queuenum,"eventtime":localtime, "servicetype":"2","tt":tt}
		request=urllib2.Request(inte, headers=headers);
		data = json.dumps(values, ensure_ascii=False)
		#获得回送的数据
		response=urllib2.urlopen(request, data);
		#print response.read()
	###########################################
	
	###########################################评价
	if random.randint(1, 10)!=1:
		waittime = waittime+random.randint(100, 200)
		t = time.localtime(time.time() + ticks + waittime)
		localtime = time.strftime("%Y-%m-%d %H:%M:%S", t) 
		tt=time.strftime("%Y%m%d%H%M%S", t) 
		data = '%s%s'%(tt, SK)
		hash_md5 = hashlib.md5(data)
		s2 = hash_md5.hexdigest()
		apprst = random.randint(0, 4)
		values={"service":"apprise","account":"ACCOUNT","password":s2,"ywlsh":ywlsh,"hallno":hallno, "bizid":bizid,"queuenum":queuenum,"eventtime":localtime, "appriseresult":apprst,"tt":tt}
		request=urllib2.Request(inte, headers=headers);
		data = json.dumps(values, ensure_ascii=False)
		#获得回送的数据
		response=urllib2.urlopen(request, data);
		#print response.read()
	###########################################
	counts-=1;

	#values={"service":"getisinblacklist","account":"ACCOUNT","password":s2,"cardid":"10010"}
	#values={"service":"getisinproxy","account":"ACCOUNT","password":s2,"cardid":"10010"}



	#values={"service":"login","account":"ACCOUNT","password":s2,"hallno":"A001","counterno":"A0011","serverno":"9","servername":"员工3","eventtime":localtime,"tt":tt}
	#values={"service":"unlogin","account":"ACCOUNT","password":s2,"hallno":"A001", "counterno":"A0011","eventtime":localtime,"tt":tt}
	#values={"service":"pause","account":"ACCOUNT","password":s2,"hallno":"A001","counterno":"A0011", "eventtime":localtime,"tt":tt}
	#values={"service":"cancelpause","account":"ACCOUNT","password":s2,"hallno":"A001","counterno":"A0011","eventtime":localtime,"tt":tt}



	#values = {"service":"getisinblacklist","account":"ACCOUNT","password":s2,"cardid":"100101"}
	#values={"service":"apprise","account":"test","hallno":"1","password":"3cfc762ec54d38703bc2208c1b60bb6a","bizid":"2","appriseresult":"0","queuenum":"B001","eventtime":"2018-09-22 09:59:29","ywlsh":"1-002-20180922095852-B001","tt":"20180922101526"}
	