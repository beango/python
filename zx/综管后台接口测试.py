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

def getstaffinfo():
	t = time.localtime()
	tt=time.strftime("%Y%m%d%H%M%S", t)  + "%03d"% random.randint(0, 999)

	data = '%s%s'%(tt, SK)
	hash_md5 = hashlib.md5(data)
	s2 = hash_md5.hexdigest()
	values={"account":"ACCOUNT","password":s2,"service":"getstaffinfo","hallno":"1","tt":tt}
	request=urllib2.Request(inte, headers=headers);
	data = json.dumps(values) # , ensure_ascii=False
	#获得回送的数据
	response=urllib2.urlopen(request, data);

	result = response.read()

	d = json.loads(result)
	print len(d["staffarray"]), time.strftime("%Y-%m-%d %H:%M:%S", t)

def devicestatus():
	t = time.localtime()
	tt=time.strftime("%Y%m%d%H%M%S", t)  + "%03d"% random.randint(0, 999)

	data = '%s%s'%(tt, SK)
	hash_md5 = hashlib.md5(data)
	s2 = hash_md5.hexdigest()
	values={"account":"ACCOUNT","password":s2, "devicemac":"mac4", "devicename":"mac4-name", "status": "无打印纸", "service":"devicestatus","hallno":"1","tt":tt}
	request=urllib2.Request(inte, headers=headers);
	data = json.dumps(values) # , ensure_ascii=False
	#获得回送的数据
	response=urllib2.urlopen(request, data);

	result = response.read()

	print result

def employeelogin():
	t = time.localtime()
	tt=time.strftime("%Y%m%d%H%M%S", t)  + "%03d"% random.randint(0, 999)

	data = '%s%s'%(tt, SK)
	hash_md5 = hashlib.md5(data)
	s2 = hash_md5.hexdigest()
	values={"service":"employeelogin","account":"ACCOUNT","password":s2,"hallNo":"1", "userrole":"2", "userid": "admin", "userpwd":"ce0bfd15059b68d67688884d7a3d3e8c","tt":tt}
	values={"service":"employeelogin","account":"ACCOUNT","password":s2,"hallNo":"1", "userrole":"1", "userid": "1", "userpwd":"49BA59ABBE56E057","tt":tt}
	request=urllib2.Request(inte, headers=headers);
	data = json.dumps(values) # , ensure_ascii=False
	#获得回送的数据
	response=urllib2.urlopen(request, data);

	result = response.read()

	print result

def employeeunlogin():
	t = time.localtime()
	tt=time.strftime("%Y%m%d%H%M%S", t)  + "%03d"% random.randint(0, 999)

	data = '%s%s'%(tt, SK)
	hash_md5 = hashlib.md5(data)
	s2 = hash_md5.hexdigest()
	values={"service":"employeeunlogin","account":"ACCOUNT","password":s2,"hallNo":"1", "userrole":"2", "userid": "admin","tt":tt}
	#values={"service":"employeeunlogin","account":"ACCOUNT","password":s2,"hallNo":"1", "userrole":"1", "userid": "1", "tt":tt}
	request=urllib2.Request(inte, headers=headers);
	data = json.dumps(values) # , ensure_ascii=False
	#获得回送的数据
	response=urllib2.urlopen(request, data);

	result = response.read()

	print result

inte = 'http://localhost:8080/sysqueueinterface'
headers={'UserAgent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)', 'Content-Type': 'application/json'};
SK = 'B548EC106017EFB2429B7528E65055E5'
print SK
loops = 1

while loops>0:
	employeeunlogin()
	loops = loops-1
	#time.sleep(2)
