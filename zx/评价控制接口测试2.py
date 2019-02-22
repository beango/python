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

inte = 'http://10.168.13.108/fsWebServiceWebHall/evaluate/sendEvaluate.action'
headers={'UserAgent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)', 'Content-Type': 'application/json'};

values={"evaluateLevel":1,"evaluateContent":"Тњвт","transitionId":"3703c86322454536be13c7346f986972","officeId":"2","evaluateUrlAddr":"/download/recorder/10D07AEA2A44-2018-11-14-15-51-43.jpg","operatorId":"100023","counterId":"10D07AEA2A44"}
request=urllib2.Request(inte, headers=headers);
params = json.dumps(values)
response=urllib2.urlopen(request, params);
data = json.loads(response.read())

print data