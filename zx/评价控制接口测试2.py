#!/usr/bin/python3
# -*- coding: utf-8 -*- 
import requests
import json
import urllib.parse
import urllib.request

inte = 'http://localhost:8082/employeeLogin.action?cardnum=10000&psw=49BA59ABBE56E057'

response = urllib.request.urlopen(inte)
print(response.read())


# request: POST
# http测试：http://httpbin.org/
data = bytes(urllib.parse.urlencode({'word':'hello'}),encoding='utf8')
response = urllib.request.urlopen(inte, data=data)
print(response.read())
