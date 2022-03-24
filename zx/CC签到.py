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


data = urllib.parse.urlencode({'email': "6588617@gmail.com", "passwd": "Zxc12345@123"})  
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br", 
    "Content-Length": bytes(len(data)),
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"
}
r=requests.post(url="https://www.cordcloud.one/auth/login",data=data, headers=headers)
retdata=r.json()
# 7. 返回CookieJar对象:
cookiejar = r.cookies
# 8. 将CookieJar转为字典：
cookiedict = requests.utils.dict_from_cookiejar(cookiejar)
# print(cookiedict)
# print(retdata)

if retdata["ret"] != 1 :
    print("登录失败：", retdata["msg"])
    exit(0)

ip = cookiedict["ip"]
expire_in = cookiedict["expire_in"]
key = cookiedict["key"]
usid = cookiedict["uid"]

inte = 'https://www.cordcloud.one/user/checkin'
headers={
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "deflate",
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    "Cookie": "uid="+usid+"; email=6588617@gmail.com; key="+key+"; ip="+ip+"; expire_in="+expire_in
    #"Content-Length": bytes(0)
}
r=requests.post(url=inte, headers=headers)
retdata = r.json()
print(time.strftime('[CC]%Y.%m.%d %H:%M:%S',time.localtime(time.time())), "--->", retdata["msg"])
print()

# sshpass -p '@@9HLx63RwWMAe' scp -r ./CC签到.py root@106.75.148.48:/root
# sshpass -p '9HLx63RwWMAe' scp -P 26807 -r CC签到.py root@144.168.63.235:/root