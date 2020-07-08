# -*- coding:utf-8 -*-
import requests
import json

host = "http://localhost:8080/appries/appriesFileupload.action"
endpoint = "post"

url = ''.join([host,endpoint])

#流式上传
#with open( 'account.py' ) as f:
#    r = requests.post(url,data = f)
r = requests.post(url)
print (r.text)
