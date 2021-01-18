#!/usr/bin/python3
# -*- coding: utf-8 -*- 
import requests
import json
import urllib
import hashlib
import sys,time,random
from datetime import datetime

inte = 'http://localhost:8003/employeeLogin2.action?f=2&name=10000&psw=49BA59ABBE56E057&mac=B002475FB11B'
headers={'UserAgent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)', 'Content-Type': 'application/json'}
# values = "{\"service\":\"addticketrecord\",\"account\":\"test\",\"hallno\":\"2\",\"password\":\"5019254caed8956a67b1d936d759d7e1\",\"bizid\":\"DL13\",\"cardtype\":\"身份证\",\"queuetype\":\"1\",\"queuenum\":\"A014\",\"cardid\":\"440184198101110622\",\"cardname\":\"钟少娟\",\"mobile\":\"\",\"yyno\":\"20200603DL1348081\",\"eventtime\":\"2020-06-03 09:08:32\",\"isproxy\":\"1\",\"counterlist\":\"2,3,4,5,6,7,8,9,10,11,24,25,26,27,28,29,30,31,32,33\",\"ywlsh\":\"204120200603090832A014\",\"tt\":\"20200603090833\"}"
# values = {"service":"addticketrecord","account":"test","hallno":"2","password":"5019254caed8956a67b1d936d759d7e1","bizid":"DL13","cardtype":"身份证","queuetype":"1","queuenum":"A014","cardid":"440184198101110622","cardname":"钟少娟","mobile":"null","yyno":"20200603DL1348081","eventtime":"2020-06-03 09:08:32","isproxy":"1","counterlist":"2,3,4,5,6,7,8,9,10","ywlsh":"204120200603090832A014","tt":"20200603090833"}
# data = bytes(json.dumps(values), encoding='utf8')
# request = urllib.request.Request(url=inte, headers=headers, data = data, method='POST')
request = urllib.request.Request(url=inte, headers=headers, method='POST')
response = urllib.request.urlopen(request)
data = response.read().decode('utf-8')
# data = eval("'{}'".format(data))
print(data)