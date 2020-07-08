#!/usr/bin/python2.7 
# -*- coding: utf-8 -*- 
import requests
import json
import urllib,urllib2
import hashlib
import sys,time,random
reload(sys)
sys.setdefaultencoding('utf8')

TOKEN_VERSION='v2'
accessKey = 'AK'
expireTime = int(time.time())+3


headers={'UserAgent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)', 'Content-Type': 'application/json'};
SK = 'B548EC106017EFB2429B7528E65055E5'
#post方式时候要发送的数据

localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
print localtime

ywlsh=time.strftime("%Y%m%d%H%M%S", time.localtime()) 
#ywlsh=20180920132113
print ywlsh

values={"account":"ACCOUNT","password":" PASSWORD","service":"addTicketRecord","hallno":"A001","bizid":"350200-XM-021","cardid":"350583198911304369","cardname":"张三","cardtype":"身份证","queuenum":"A0001","queuetype":"0","ywlsh":ywlsh,"eventtime":localtime,"tt":ywlsh,"isproxy":"1"}
#values={"service":"Call","account":"ACCOUNT","password":" PASSWORD","ywlsh":ywlsh,"hallno":"A001", "bizid":"350200-XM-021","queuenum":"A0001","eventtime":localtime,"userid":"2","windowno":"A0011","tt":"20170808165301"}
#values={"service":"service","account":"ACCOUNT","password":" PASSWORD","ywlsh":ywlsh,"hallno":"A001","bizid":"350200-XM-021","queuenum":"A0001","eventtime":localtime, "servicetype":"1","tt":"20170808165301"}
#values={"service":"service","account":"ACCOUNT","password":" PASSWORD","ywlsh":ywlsh,"hallno":"A001","bizid":"350200-XM-021","queuenum":"A0001","eventtime":localtime, "servicetype":"2","tt":"20170808165301"}
#values={"service":"apprise","account":"ACCOUNT","password":" PASSWORD","ywlsh":ywlsh,"hallno":"A001", "bizid":"350200-XM-021","queuenum":"A0001","eventtime":localtime, "appriseresult":"1","tt":"20170808165301"}

#values={"service":"getisinblacklist","account":"ACCOUNT","password":" PASSWORD","cardid":"10010"}
#values={"service":"getisinproxy","account":"ACCOUNT","password":" PASSWORD","cardid":"10010"}



#values={"service":"login","account":"ACCOUNT","password":"PASSWORD","hallno":"A001","counterno":"1","serverno":"8","servername":"服务员工2","eventtime":localtime,"tt":"20170808165301"}
#values={"service":"unlogin","account":"ACCOUNT","password":" PASSWORD","hallno":"A001", "counterno":"1","eventtime":localtime,"tt":"20170808165301"}
#values={"service":"pause","account":"ACCOUNT","password":" PASSWORD","hallno":"A001","counterno":"1", "eventtime":localtime,"tt":"20170808165301"}
#values={"service":"cancelpause","account":"ACCOUNT","password":" PASSWORD","hallno":"A001","counterno":"1","eventtime":localtime,"tt":"20170808165301"}



#values = {"service":"getisinblacklist","account":"ACCOUNT","password":" PASSWORD","cardid":"100101"}

data =  '|SK|%s|' % (json.dumps(values, ensure_ascii=False))

hash_md5 = hashlib.md5(data)
s2 = "%s-%s" % (TOKEN_VERSION, hash_md5.hexdigest())


data = '%s%s'%(ywlsh, SK)
print 'token数据：' + data
hash_md5 = hashlib.md5(data)
s2 = hash_md5.hexdigest()
data = json.dumps(values, ensure_ascii=False) 
#对发送的数据进行编码
#data=urllib.urlencode(values);
print s2
#发送一个http请求
request=urllib2.Request("http://localhost:8080/sysqueueinterface?token=" + s2, headers=headers);

#获得回送的数据
response=urllib2.urlopen(request, data);

print response.read()

