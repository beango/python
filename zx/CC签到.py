#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
import json
import urllib
import hashlib
import sys,time,random
import zlib, gzip
from http import cookiejar
from datetime import datetime 

data = {"email": U"6588617@gmail.com", "passwd": U"Zxc12345@#123", "code": ""}
# data = bytes(urllib.parse.urlencode(data), encoding='utf8')
# data = bytes("email=6588617@gmail.com&passwd=Zxc12345@&code=", encoding='utf8')
data = urllib.parse.urlencode({'email': "6588617@gmail.com", "passwd": "Zxc12345@#123", 'code':''})  
# data = data.encode('utf-8')  
data = bytes(data, encoding='utf8')
print (data)
headers = {
    # "expire_in": str(time.time()),
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "deflate", 
    "Accept-Language": "zh-CN,en-US;q=0.5",
    "Connection": "keep-alive",
    "Content-Length": len(data),
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
    # "Cookie": "__cfduid=d08b3c34d430cf2144ee39de2f65327281593737708; crisp-client%2Fsession%2Ff24e0785-07d5-4a5f-961b-bde1c9b6245b=session_dcfd2417-f774-402f-a285-1e172174300e",
    "Host":"www.cordcloud.pro",
    "Origin": "https://www.cordcloud.pro",
    "Referer": "https://www.cordcloud.pro/auth/login", 
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
}
request = urllib.request.Request(url="https://www.cordcloud.pro/auth/login", data = data, headers=headers, method='POST')
cookie = cookiejar.CookieJar()#将cookie声明为一个CookieJar对象
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
response = opener.open(request)
#print(response.read())
#gzipFile = gzip.GzipFile(fileobj=response)
#print( gzipFile.read().decode())
retdata = json.loads(response.read()) #response.read().decode() # 
# print(cookie)

if retdata["ret"] != 1 :
    print("登录失败：", retdata["msg"])
    exit(0)
ip = ""
expire_in = 0
key = ""
usid = ""
cfduid=""
for item in cookie:
    if item.name == "ip":
        ip = item.value
    if item.name == "expire_in":
        expire_in = item.value
    if item.name == "key":
        key = item.value
    if item.name == "uid":
        usid = item.value
    if item.name == "__cfduid":
        cfduid = item.value
inte = 'https://www.cordcloud.pro/user/checkin'
headers={
    "Host": "www.cordcloud.pro",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,en-US;q=0.5",
    "Accept-Encoding": "deflate",
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive",
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    "Cookie1": "_ga=GA1.2.380391384.1579057478; uid="+usid+"; email=6588617%40gmail.com; key="+key+"; ip="+ip+"; expire_in="+expire_in,
    "Cookie": "uid="+usid+"; email=6588617@gmail.com; key="+key+"; ip="+ip+"; expire_in="+expire_in,
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Length": 0
}
# print(headers)
request = urllib.request.Request(url=inte, headers=headers, method='POST')
response=urllib.request.urlopen(request)
retdata=response.read()
retdata = json.loads(retdata)
# gzipFile = gzip.GzipFile(fileobj=response)
# retdata = gzipFile.read().decode()
# retdata = json.loads(retdata)
print(time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time())), "--->", retdata["msg"])
