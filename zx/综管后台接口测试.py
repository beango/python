#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import requests
import json
import urllib2, hashlib
import sys,time,random
from datetime import datetime

headers = {'UserAgent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)', 'Content-Type': 'application/json'}

def getstaffinfo():
	t = time.localtime()
	tt=time.strftime("%Y%m%d%H%M%S", t)  + "%03d"% random.randint(0, 999)

	data = '%s%s'%(tt, SK)
	hash_md5 = hashlib.md5(data)
	s2 = hash_md5.hexdigest()
	values={"account":"ACCOUNT","password":s2,"service":"getstaffinfo","hallno":"1","tt":tt}
	request=urllib2.Request(inte, headers=headers)
	data = json.dumps(values) # , ensure_ascii=False
	#获得回送的数据
	response=urllib2.urlopen(request, data)

	result = response.read()

	d = json.loads(result)
	print (len(d["staffarray"]), time.strftime("%Y-%m-%d %H:%M:%S", t))

def devicestatus():
	t = time.localtime()
	tt=time.strftime("%Y%m%d%H%M%S", t)  + "%03d"% random.randint(0, 999)

	data = '%s%s'%(tt, SK)
	hash_md5 = hashlib.md5(data)
	s2 = hash_md5.hexdigest()
	values={"account":"ACCOUNT","password":s2, "devicemac":"mac4", "devicename":"mac4-name", "status": "无打印纸", "service":"devicestatus","hallno":"1","tt":tt}
	request=urllib2.Request(inte, headers=headers)
	data = json.dumps(values) # , ensure_ascii=False
	#获得回送的数据
	response=urllib2.urlopen(request, data)

	result = response.read()

	print (result)

def employeelogin():
	t = time.localtime()
	tt=time.strftime("%Y%m%d%H%M%S", t)  + "%03d"% random.randint(0, 999)

	data = ('%s%s'%(tt, SK))
	hash_md5 = hashlib.md5(data.encode("utf8"))
	s2 = hash_md5.hexdigest()
	values={"service":"employeelogin","account":"ACCOUNT","password":s2,"hallNo":"1", "userrole":"2", "userid": "admin", "userpwd":"E10adc3949ba59abbe56e057f20f883e","tt":tt}
	values={"service":"employeelogin","account":"ACCOUNT","password":s2,"hallNo":"1", "userrole":"1", "userid": "2", "userpwd":"49ba59ABBE56E057","tt":tt}
	request=urllib2.Request(inte, headers=headers)
	data = json.dumps(values) # , ensure_ascii=False
	#获得回送的数据
	data = data.encode('utf-8')
	response=urllib2.urlopen(request, data)
	result = response.read().decode("utf8")
	print (result)

def login():
	t = time.localtime()
	tt=time.strftime("%Y%m%d%H%M%S", t)  + "%03d"% random.randint(0, 999)

	data = '%s%s'%(tt, SK)
	hash_md5 = hashlib.md5(data)
	s2 = hash_md5.hexdigest()
	values={"service":"login","account":"test","hallno":"2","password":"0015f6c7edde7360ec289ca12d496050","counterno":"19","serverno":"1133","servername":"樊廷振","eventtime":"2019-05-27 08:50:26","tt":"20190527085306"}
	request=urllib2.Request(url = inte, headers=headers)
	data = json.dumps(values) # , ensure_ascii=False
	#获得回送的数据
	response=urllib2.urlopen(request, data)
	result = response.read()
	print (result)


def test():
	t = time.localtime()
	tt=time.strftime("%Y%m%d%H%M%S", t)  + "%03d"% random.randint(0, 999)

	data = '%s%s'%(tt, SK)
	hash_md5 = hashlib.md5(data)
	s2 = hash_md5.hexdigest()
	values={"service":"login","account":"test","hallno":"2","password":"0015f6c7edde7360ec289ca12d496050","counterno":"19","serverno":"1133","servername":"樊廷振","eventtime":"2019-05-27 08:50:26","tt":"20190527085306"}
	request=urllib2.Request(url = "http://shenbao.dg.gov.cn/yjhapi/api/token?time=2019-08-13_11:04:14.14&policyName=11&loginSign=a6a47e06509532e38f1788c34acec5bf", headers=headers)
	data = json.dumps(values) # , ensure_ascii=False
	data = ""
	#获得回送的数据
	response=urllib2.urlopen(request, data)
	result = response.read()
	print (result)

def login2():
	t = time.localtime()
	tt=time.strftime("%Y%m%d%H%M%S", t)  + "%03d"% random.randint(0, 999)

	data = '%s%s'%(tt, SK)
	hash_md5 = hashlib.md5(data)
	s2 = hash_md5.hexdigest()
	values={"cardnum":"login","psw":"test"}
	request=urllib2.Request(url = "http://localhost:8080/employeeLogin.action")
	data = json.dumps(values) # , ensure_ascii=False
	#获得回送的数据
	response=urllib2.urlopen(request, "cardnum=test&psw=test")
	result = response.read()
	print (result)

inte = 'http://localhost:8080/sysqueueinterface'

SK = 'B548EC106017EFB2429B7528E65055E5'
login2()
