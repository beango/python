#!/usr/bin/python
#coding=utf-8
 
import urllib.request
import urllib.parse
import random 
import time
import datetime
import json

uri = 'http://localhost:8080/appriesAddSpByPantryn'
idcard = ['44116','1158']
mac = ['17','2']
headers = {'Accept-Charset': 'utf-8', 'Content-Type': 'application/json'}

i = 1
count = 1
t = datetime.datetime.strptime("2020-11-26 8:36:00", "%Y-%m-%d %H:%M:%S")
while i<=count:
	r = random.randint(100, 170)
	t = t + datetime.timedelta(seconds = r)
	params = {}
	params['tt'] = t.strftime("%Y-%m-%d %H:%M:%S")
	params['mac'] = mac[random.randint(0, len(mac)-1)]
	params['cardnum'] = idcard[random.randint(0, len(idcard)-1)]
	params['pj'] = random.randint(0, 3)
	params['idcard'] = ''
	params['ywlsh'] = ''
	es_params = urllib.parse.quote_plus(json.dumps(params)).encode(encoding='utf-8')
	request = urllib.request.Request(url=uri, data = es_params,headers=headers, method='POST')
	reponse = urllib.request.urlopen(request).read()
	print(reponse)
	i+=1



