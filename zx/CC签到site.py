#!/usr/bin/python
# -*- coding: utf-8 -*- 
import requests
import json
import urllib
import hashlib
import sys,time,random
import zlib
from http import cookiejar
from datetime import datetime 

values = {"email": U"6588617@gmail.com", "passwd": U"Zxc12345@", "code": "", "remember_me": "week"}
data = bytes(urllib.parse.urlencode(values), encoding='utf8')
print (data)
headers = {
    "expire_in": str(time.time()),
}
request = urllib.request.Request(url="https://www.cordcloud.pro/auth/login", data = data, headers=headers, method='POST')
cookie =cookiejar.CookieJar()#将cookie声明为一个CookieJar对象
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
response = opener.open(request)
retdata = json.loads(response.read().decode())

if retdata["ret"] !=1 :
    print("登录失败：", retdata["msg"])
    exit(0)
ip = ""
expire_in = 0
key = ""
for item in cookie:
    if item.name == "ip":
        ip = item.value
    if item.name == "expire_in":
        expire_in = item.value
    if item.name == "key":
        key = item.value
        
inte = 'https://www.cordcloud.pro/user/checkin'
headers={
    "Host": "www.cordcloud.pro",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,en-US;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive",
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    "Cookie": "_ga=GA1.2.380391384.1579057478; uid=29458; email=6588617%40gmail.com; key="+key+"; ip="+ip+"; expire_in="+expire_in,
    "Cookie1": "__cfduid=d08b3c34d430cf2144ee39de2f65327281593737708; crisp-client%2Fsession%2Ff24e0785-07d5-4a5f-961b-bde1c9b6245b=session_84dd69ee-be9e-43c2-b0b5-a2944d037865",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Content-Length": 0
}
request = urllib.request.Request(url=inte, headers=headers, method='POST')
response=urllib.request.urlopen(request)
print(response.read())
retdata = json.loads(response.read().decode())
print(time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time())), "--->", retdata["msg"], retdata["ret"], "签到成功" if(retdata["ret"]!="1") else "签到失败")
