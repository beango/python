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
from urllib import quote
import threading 
import time
num = 0

def test1():
    inte = 'http://192.168.1.171:8082/regUserInfo'
    headers={'UserAgent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)', 'Content-Type': 'application/json'}

    values={"interfacename":"regUserInfo","mobilePhone":"13688889991","password":"HBZWmm88888888","idCard":"432503197808087673","name":"刘勇伟","froms":"5"}
    request=urllib2.Request(inte, headers=headers)
    params = json.dumps(values)
    response=urllib2.urlopen(request, params)
    # data = json.loads()

    print response.read()

def test2():
    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    data.append('--%s' % boundary)
        
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'username')
    data.append('jack')
    data.append('--%s' % boundary)
        
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'mobile')
    data.append('13800138000')
    data.append('--%s' % boundary)
        
    fr=open(r'/work/workspace/文档/江门政务服务叫号机/硬件界面规范资料/02评价器/参考实现/星星.xcf','rb')
    data.append('Content-Disposition: form-data; name="%s"; filename="b.png"' % 'profile')
    data.append('Content-Type: %s\r\n' % 'image/png')
    data.append(fr.read())
    fr.close()
    data.append('--%s--\r\n' % boundary)
    
    http_url='http://10.15.0.28:8080/client/upload.htm'
    http_body='\r\n'.join(data)
    try:
        #buld http request
        req=urllib2.Request(http_url, data=http_body)
        #header
        req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
        req.add_header('User-Agent','Mozilla/5.0')
        req.add_header('Referer','http://remotserver.com/')
        #post data to server
        resp = urllib2.urlopen(req, timeout=5)
        #get response
        qrcont=resp.read()
        print qrcont
        
    except Exception,e:
        print 'http error'

#mutex = threading.Lock()
class MyThread(threading.Thread):
	def run(self):
		global num
		#上锁
		mutexFlage = mutex.acquire()
		print('线程(%s)的锁状态为%d' %(self.name, mutexFlage))
		#判断是否上锁成功
		if mutexFlage:
			num = num + 1
			time.sleep(1)
			msg = self.name + 'set num to' + str(num)
			print(msg)
			print(threading.currentThread(), threading.activeCount())
			mutex.release()

class MyThread2(threading.Thread):
	def run(self):
		for i in range(1):
			test2();

def test():
	t = MyThread2()
	# print(threading.currentThread(), threading.activeCount())
	t.start()
 
if __name__ == '__main__':
	test();

