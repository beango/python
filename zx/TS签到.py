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


data = urllib.parse.urlencode({"code":"6588617","pass":"Zxc12345@","invite":""}) 
data = "{\"code\":\"6588617\",\"pass\":\"Zxc12345@\",\"invite\":\"\"}"
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,en-US;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Content-Length": bytes(len(data)),
    "Content-Type":"application/json; charset=UTF-8"
}
r=requests.post(url="http://39.103.128.252:3333/api/auth/login", data=data, headers=headers)
retdata=r.json()
cookiejar = r.cookies
cookiedict = requests.utils.dict_from_cookiejar(cookiejar)
# print(retdata)

if retdata["code"] != 200 :
    print("登录失败：", retdata["msg"])
    exit(0)

token = retdata["data"]["token"]
# print(token)

inte = 'http://39.103.128.252:3333/api/auth/sign'
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,en-US;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    # "Content-Length": "0",
    "Content-Type":"application/json; charset=UTF-8",
    "Authorization": "Bearer " + token,
    "Connection": "keep-alive"
}
r=requests.post(url=inte, headers=headers)
retdata = r.json()
# print(retdata)
print(time.strftime('[TS]%Y.%m.%d %H:%M:%S',time.localtime(time.time())), "--->", retdata)

# sshpass -p '@@9HLx63RwWMAe' scp -r ./TS签到.py root@106.75.148.48:/root
# sshpass -p '9HLx63RwWMAe' scp -P 26807 -r TS签到.py root@144.168.63.235:/root