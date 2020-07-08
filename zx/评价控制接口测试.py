#!/usr/bin/python2.7 
# -*- coding: utf-8 -*- 
import requests
import json
import urllib
import hashlib
import sys,time,random
from datetime import datetime 

inte = 'http://localhost:8081/evalctl'
headers={'UserAgent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)', 'Content-Type': 'application/json'}

values={"method":"STATE_EVALUATE", "json":"{\"centerid\":\"000001\",\"id\":\"9c1c3ffd-551b-4644-9c9b-57956c6e0b90\",\"counterid\":\"44060500000001Window0101\",\"serviceper_no\":\"1\",\"state\":0}"}
request=urllib.request.Request(inte, headers=headers)
params = bytes(json.dumps(values), encoding="utf-8")
response=urllib.request.urlopen(request, params)
data = json.loads(response.read())

print(data["code"])
print(data["context"]["msg"])


values={"method":"STATE_EVALUATE", "json":"{\"centerid\":\"000001\",\"id\":\"9c1c3ffd-551b-4644-9c9b-57956c6e0b90\",\"counterid\":\"44060500000001Window0101\",\"serviceper_no\":\"008201\",\"state\":7}"}
request=urllib.request.Request(inte, headers=headers)
params = json.dumps(values)
response=urllib.request.urlopen(request, params)
data = json.loads(response.read())