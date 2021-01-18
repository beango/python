#!/usr/bin/python2.7 
# -*- coding: utf-8 -*- 
import requests
import json
import urllib
import urllib.request
import http.cookiejar
import hashlib
import sys,time,random,re
from datetime import datetime

inte = 'http://localhost:8080/sysqueueinterface'
intedata = "http://localhost:8080/gethalldata.action?istest=1"
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
headers = {
	#'Connection':'keep-alive',
	#'Upgrade-Insecure-Requests':'1',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
	'Content-Type': 'application/json;charset=UTF-8',
	#'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	#'Accept-Language':'zh-CN,zh;q=0.9',
	'Cookie':'user.cookie="admin,c4ca4238a0b923820dcc509a6f75849b"'
}
request = urllib.request.Request(url=intedata, headers=headers, method='GET')
response = urllib.request.urlopen(request)
data = response.read().decode('utf-8')
data = re.sub(r'\\','', data)
#data = re.sub(r'"','', data)
data = eval("'{}'".format(data))
data = data[1:-1]

param = json.loads(data)
# print(param)
#opener = urllib2.build_opener()
#opener.addheaders.append(('Cookie', 'user.cookie="admin,c4ca4238a0b923820dcc509a6f75849b,ç³»ç»"'))
#r = opener.open(intedata)
#param = json.loads(json.loads(r.read()))
#r.close()
#opener.close()
counts = 100 #执行次数2018-09-29 14:56:40.000
a1=(2020, 11, 27, 9,0,0,0,0,0)
a2=(2020, 11, 27, 17,59,59,0,0,0) 
start=time.mktime(a1)    #生成开始时间戳
end=time.mktime(a2)      #生成结束时间戳

while counts>0:
	counts-=1
	#ticks = (datetime.now() - datetime.strptime('2018-08-02 8:56:59.000',"%Y-%m-%d %H:%M:%S.%f")).total_seconds() * -1 #生成N秒前的数据

	queueobj = queue[random.randint(0, len(queue)-1)]
	queuenum = queueobj["queuenum"]
	queuetype = queueobj["queuetype"]
	#print queuenum, queuetype
	d1 = param[random.randint(0, len(param)-1)]
	hallno = d1["hallno"]
	bizlist = d1["bizlist"]
	if len(bizlist) > 0:
		bizid = bizlist[random.randint(0, len(bizlist)-1)]
	else:
		bizid = ""
	counterlist = d1["counterlist"]
	if len(counterlist)==0:
		continue
	counterid = counterlist[random.randint(0, len(counterlist)-1)]
	elist = d1["elist"]
	eid = elist[random.randint(0, len(elist)-1)]
	
	#print hallno, bizid, counterid, eid

	t1=random.randint(start,end)
	t = time.localtime(t1)
	localtime = time.strftime("%Y-%m-%d %H:%M:%S", t) 
	ywlsh=time.strftime("%Y%m%d%H%M%S", t)  + "%03d"% random.randint(0, 999)
	#ywlsh=20180924101743
	tt = ywlsh


	###########################################取号
	data = '%s%s'%(ywlsh, SK)
	hash_md5 = hashlib.md5(data.encode("utf-8"))
	s2 = hash_md5.hexdigest()
	values={"account":"ACCOUNT","password":s2,"service":"addticketrecord","hallno":hallno,"bizid":bizid,"cardid":ywlsh,"cardname":u"张三","cardtype":u"身份证","queuenum":queuenum,"queuetype":queuetype,"ywlsh":ywlsh,"eventtime":localtime,"tt":tt,"isproxy":random.randint(0,1),"mobile":"1234567890"}
	#values={"service":"addticketrecord","hallno":"TEST","password":s2,"BizID":"3","bizname":"комплексная операция","CardType":"other","QueueType":"1","QueueNum":"A002","CardID":u"операция","cardname":u"операция","mobile":"123456789","EventTime":"2020-04-09 09:35:15","counterlist":"1,2,3","ywlsh":"TEST-001-20200409093518-A002","isproxy":"0","tt":tt}
	#data = json.dumps(values) # , ensure_ascii=False
	data = bytes(json.dumps(values), encoding='utf8')
	request = urllib.request.Request(url=inte, headers=headers, data = data, method='POST')
	response = urllib.request.urlopen(request)
	data = response.read().decode('utf-8')
	data = eval("'{}'".format(data))
	# data = data[1:-1]
	print(json.loads(data))
	#continue
	###########################################
	
	###########################################叫号
	waittime = random.randint(100, 200)
	t = time.localtime(t1 + waittime)
	localtime = time.strftime("%Y-%m-%d %H:%M:%S", t) 
	tt=time.strftime("%Y%m%d%H%M%S", t) 
	data = '%s%s'%(tt, SK)
	hash_md5 = hashlib.md5(data.encode("utf-8"))
	s2 = hash_md5.hexdigest()
	isabort = random.randint(1, 25)!=1
	if isabort:
		values={"service":"call","account":"ACCOUNT","password":s2,"ywlsh":ywlsh,"hallno":hallno, "bizid":bizid,"queuenum":queuenum,"eventtime":localtime,"userid":eid,"windowno":counterid,"tt":tt}
		data = bytes(json.dumps(values, ensure_ascii=False), encoding='utf8')
		request = urllib.request.Request(url=inte, headers=headers, data = data, method='POST')
		response=urllib.request.urlopen(request)
		
		###########################################开始办理
		if random.randint(1, 30)!=1:
			waittime = waittime+random.randint(100, 200)
			t = time.localtime(t1 + waittime)
			localtime = time.strftime("%Y-%m-%d %H:%M:%S", t) 
			tt=time.strftime("%Y%m%d%H%M%S", t) 
			data = '%s%s'%(tt, SK)
			hash_md5 = hashlib.md5(data.encode("utf-8"))
			s2 = hash_md5.hexdigest()
			values={"service":"service","account":"ACCOUNT","password":s2,"ywlsh":ywlsh,"hallno":hallno,"bizid":bizid,"queuenum":queuenum,"eventtime":localtime, "servicetype":"1","tt":tt}
			data = bytes(json.dumps(values, ensure_ascii=False), encoding='utf8')
			request = urllib.request.Request(url=inte, headers=headers, data = data, method='POST')
			response = urllib.request.urlopen(request)
			#print response.read()
		###########################################

	else:
		print('没有叫号')
	###########################################
	
	

	###########################################结束办理
	if random.randint(1, 30)!=1:
		waittime = waittime+random.randint(100, 200)
		t = time.localtime(t1 + waittime)
		localtime = time.strftime("%Y-%m-%d %H:%M:%S", t) 
		tt=time.strftime("%Y%m%d%H%M%S", t) 
		data = '%s%s'%(tt, SK)
		hash_md5 = hashlib.md5(data.encode("utf-8"))
		s2 = hash_md5.hexdigest()
		values={"service":"service","account":"ACCOUNT","password":s2,"ywlsh":ywlsh,"hallno":hallno,"bizid":bizid,"queuenum":queuenum,"eventtime":localtime, "servicetype":"2","tt":tt}
		data = bytes(json.dumps(values, ensure_ascii=False), encoding='utf8')
		request = urllib.request.Request(url=inte, headers=headers, data = data, method='POST')
		response = urllib.request.urlopen(request)
	###########################################
	
	###########################################评价
	if random.randint(1, 30)!=1:
		waittime = waittime+random.randint(100, 200)
		t = time.localtime(t1 + waittime)
		localtime = time.strftime("%Y-%m-%d %H:%M:%S", t) 
		tt=time.strftime("%Y%m%d%H%M%S", t) 
		data = '%s%s'%(tt, SK)
		hash_md5 = hashlib.md5(data.encode("utf-8"))
		s2 = hash_md5.hexdigest()
		apprst = random.randint(0, 6)
		# apprst = 4
		values={"service":"apprise","account":"ACCOUNT","password":s2,"ywlsh":ywlsh,"hallno":hallno, "bizid":bizid,"queuenum":queuenum,"eventtime":localtime, "appriseresult":apprst,"tt":tt}
		data = bytes(json.dumps(values, ensure_ascii=False), encoding='utf8')
		request = urllib.request.Request(url=inte, headers=headers, data = data, method='POST')
		response = urllib.request.urlopen(request)
		#print response.read()
	###########################################

	#values={"service":"getisinblacklist","account":"ACCOUNT","password":s2,"cardid":"10010"}
	#values={"service":"getisinproxy","account":"ACCOUNT","password":s2,"cardid":"10010"}



	#values={"service":"login","account":"ACCOUNT","password":s2,"hallno":"A001","counterno":"A0011","serverno":"9","servername":"员工3","eventtime":localtime,"tt":tt}
	#values={"service":"unlogin","account":"ACCOUNT","password":s2,"hallno":"A001", "counterno":"A0011","eventtime":localtime,"tt":tt}
	#values={"service":"pause","account":"ACCOUNT","password":s2,"hallno":"A001","counterno":"A0011", "eventtime":localtime,"tt":tt}
	#values={"service":"cancelpause","account":"ACCOUNT","password":s2,"hallno":"A001","counterno":"A0011","eventtime":localtime,"tt":tt}



	#values = {"service":"getisinblacklist","account":"ACCOUNT","password":s2,"cardid":"100101"}
	#values={"service":"apprise","account":"test","hallno":"1","password":"3cfc762ec54d38703bc2208c1b60bb6a","bizid":"2","appriseresult":"0","queuenum":"B001","eventtime":"2018-09-22 09:59:29","ywlsh":"1-002-20180922095852-B001","tt":"20180922101526"}
	
