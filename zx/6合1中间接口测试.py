#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import requests
import json
import urllib2, hashlib, urllib
import sys,time,random
from datetime import datetime
import base64

headers = {'UserAgent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)', 'Content-Type': 'application/json'}

def sms():
	values={"mobile":"25C11","content":"test"}
	request=urllib2.Request(url = smsinterface, headers=headers)
	data = json.dumps(values) # , ensure_ascii=False
	print data
	#获得回送的数据
	response=urllib2.urlopen(request, data)
	result = response.read()
	print (result)

def test_mid():
	values={"interfacename":"25C11","sbkzjsjip":"68.36.18.216","ywckjsjip":"68.36.18.11","qhxxxlh":"1909064401000001000001","pdh":"000001"
	,"ywlb":"01","qhrxm":"樊廷振","sfzmhm":"","dlrsfzmhm":"","qhsj":"2019-05-27 08:53:06","rylb":"1"}
	request=urllib2.Request(url = midqueueinterface, headers=headers)
	data = json.dumps(values) # , ensure_ascii=False
    #data = ""
	#获得回送的数据
	response=urllib2.urlopen(request, data)
	result = response.read()
	print (result)

def call():
	reqdata = {"ywckjsjip":"192.168.1.126","glbm":"004"}
	data = {"opType": "TMRI_CALLOUT", "charset": "utf-8", "reqdata": reqdata}
	request=urllib2.Request(url = queueinterface, headers=headers)
	print data
	#获得回送的数据
	response=urllib2.urlopen(request, json.dumps(data))
	print response.getcode()
	print response.geturl()
	print response.read()

def recall():
	reqdata = {"qhxxxlh":"190905440100000100Y0110"}
	data = {"opType": "TMRI_RECALL", "charset": "utf-8", "reqdata": base64.b64encode(json.dumps(reqdata))}
	request=urllib2.Request(url = queueinterface, headers=headers)
	print data
	#获得回送的数据
	response=urllib2.urlopen(request, urllib.urlencode(data))
	print response.getcode()
	print response.geturl()
	print response.read()

def eval():
	reqdata = {"qhxxxlh":"190905440100000100Y011"}
	data = {"opType": "TMRI_EVALUATION", "charset": "utf-8", "reqdata": base64.b64encode(json.dumps(reqdata))}
	request=urllib2.Request(url = queueinterface, headers=headers)
	print data
	#获得回送的数据
	response=urllib2.urlopen(request, urllib.urlencode(data))
	print response.getcode()
	print response.geturl()
	print response.read()

def skip():
	reqdata = {"qhxxxlh":"190905440100000100Y011"}
	data = {"opType": "TMRI_SKIP", "charset": "utf-8", "reqdata": base64.b64encode(json.dumps(reqdata))}
	request=urllib2.Request(url = queueinterface, headers=headers)
	print data
	#获得回送的数据
	response=urllib2.urlopen(request, urllib.urlencode(data))
	print response.getcode()
	print response.geturl()
	print response.read()

def pause():
	params = "{\"opType\":\"TMRI_SUSPEND\",\"charset\":\"utf-8\",\"reqdata\":\"\"}"
	req = urllib2.Request(queueinterface, params)    #生成页面请求的完整数据
	response = urllib2.urlopen(req)     #发送页面请求

	print response.getcode()
	print response.geturl()
	print response.read()

def resume():
	reqdata = {"ywckjsjip":"192.168.1.121"}
	data = {"opType": "TMRI_RECOVER", "charset": "utf-8", "reqdata": base64.b64encode(json.dumps(reqdata))}
	request=urllib2.Request(url = queueinterface, headers=headers)
	print data
	#获得回送的数据
	response=urllib2.urlopen(request, urllib.urlencode(data))
	print response.getcode()
	print response.geturl()
	print response.read()

def receive():
	reqdata = {"lsh":"201909050001", "xm": "张三", "pzlx": "1", "zzjsjip": "192.168.1.121" , "lzckbh": "4401000001"}
	data = {"opType": "TMRI_RECEIVE", "charset": "utf-8", "reqdata": base64.b64encode(json.dumps(reqdata))}
	request=urllib2.Request(url = queueinterface, headers=headers)
	print data
	#获得回送的数据
	response=urllib2.urlopen(request, urllib.urlencode(data))
	print response.getcode()
	print response.geturl()
	print response.read()

def test():
	t = time.localtime()
	tt=time.strftime("%Y%m%d%H%M%S", t)  + "%03d"% random.randint(0, 999)

	data = '%s%s'%(tt, SK)
	values={"interfacename":"25C11","sbkzjsjip":"68.36.18.216","ywckjsjip":"68.36.18.11", "qhxxxlh": "1909064401000001000001", "pdh": "000001", "ywlb": "01","qhrxm": "樊廷振", "sfzmhm":"", "dlrsfzmhm":"", "qhsj":"2019-05-27 08:53:06","rylb":"1"}
	request=urllib2.Request(url = testinterface, headers=headers)
	data = json.dumps(values) # , ensure_ascii=False
    #data = ""
	#获得回送的数据
	response=urllib2.urlopen(request, data)
	result = response.read()
	print (result)

midqueueinterface = 'http://localhost:8089/midlequeueinterface'
queueinterface = 'http://localhost:8089/queue'
smsinterface = 'http://localhost:8089/sms'
testinterface = 'http://localhost:23412'

SK = 'B548EC106017EFB2429B7528E65055E5'
#resume  call  pause  recall  eval  skip  receive

test_mid()