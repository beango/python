#!/usr/bin/python
#coding=utf-8
 
import sys,urllib
import random 
import time
import datetime
import json

headers = {'Content-Type': 'application/json'}
uri = 'http://localhost:8080/queueInterface'
#uri = "http://111.230.14.84:8088/queueSysinterface.aspx"
#uri = "http://localhost:8080/queuectl"

i = 50001
count = random.randint(150, 170)
t = datetime.datetime.strptime("2018-07-02 8:40:00", "%Y-%m-%d %H:%M:%S")
count = 0

if i<=50000:
	params = "{\"interfacename\":\"getserverinfo\",\"serverno\":\"1\"}" # urllib.urlencode(params)
	req = urllib2.Request(uri, params)
	time.sleep(0.01)

	count += 1
	i+=1
	


def getlcddeviceprams():
	params = "{\"interfacename\":\"getlcddeviceprams\",\"devicemac\":\"301F9A644D4D\"}"
	req = urllib2.Request(uri, params)   
	response = urllib2.urlopen(req)    
	print(response.read())

def getcounterwaitpersons():
	params = "{\"interfacename\":\"getcounterwaitpersons\",\"counterno\":\"1\"}" # urllib.urlencode(params)
	req = urllib2.Request(uri, params)
	response = urllib2.urlopen(req)
	print(response.read())

def getnextnumber():
	data = {"interfacename":"getnextnumber","counterno":"1"}
	req = urllib2.Request(url=uri, headers=headers, data=json.dumps(data))
	response = urllib2.urlopen(req)
	print(response.read())

def countereventaction():
	params = "{\"interfacename\":\"countereventaction\",\"counterno\":1,\"serialid\":0,\"staffid\":\"1\",\"transcodeid\":\"\",\"eventid\":1,\"number\":\"A012\",\"markscore\":\"0\"}" # urllib.urlencode(params)
	req = urllib2.Request(uri, params)
	response = urllib2.urlopen(req)
	print(response.read())


def counterpushaction():
	params = {"interfacename":"counterpushaction","counterno":1,"staffid":"1","eventid":10}
	req = urllib2.Request(url=uri, headers=headers, data=json.dumps(params))
	response = urllib2.urlopen(req)
	print(response.read())

def getcounterinfo():
	params = "{\"interfacename\":\"getcounterinfo\",\"counterno\":\"1\"}"
	req = urllib2.Request(uri, params)
	response = urllib2.urlopen(req) 
	print(response.read())

def getserialarray():
	params = {"interfacename":"getserialarray"}
	req = urllib2.Request(url=uri, headers=headers, data=json.dumps(params))
	response = urllib2.urlopen(req) 
	print(response.read())

def getserialinfo():
	params = {"interfacename":"getserialinfo", "serialid":"123"}
	req = urllib2.Request(url=uri, headers=headers, data=json.dumps(params))
	response = urllib2.urlopen(req) 
	print(response.read())

def getcounterarray():
	params = {"interfacename":"getcounterarray"}
	req = urllib2.Request(url=uri, headers=headers, data=json.dumps(params))
	response = urllib2.urlopen(req) 
	print(response.read())

def getdatetime():
	params = {"interfacename":"getdatetime"}
	req = urllib2.Request(url=uri, headers=headers, data=json.dumps(params))
	response = urllib2.urlopen(req) 
	print(response.read())

def counterlogin():
	params = {"interfacename":"counterlogin","counterno":"1","staffid":"1","password":""}
	req = urllib2.Request(url=uri, headers=headers, data=json.dumps(params))
	response = urllib2.urlopen(req)
	print(response.read())

def getreport():
	params = {"interfacename":"getreport","datatype":"report_month_counter_serialnums","counterno":"1"}
	req = urllib2.Request(url=uri, headers=headers, data=json.dumps(params))
	response = urllib2.urlopen(req)
	print(response.read())

getreport();