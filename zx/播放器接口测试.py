#!/usr/bin/python
#coding=utf-8
 
import urllib,urllib2
import random 
import time
import datetime

uri = 'http://192.168.1.199:8083/queueSysinterface.aspx'
uri = "http://111.230.14.84:8088/queueSysinterface.aspx"
uri = "http://localhost:8080/queuectl"
i = 1
count = random.randint(150, 170)
t = datetime.datetime.strptime("2018-07-02 8:40:00", "%Y-%m-%d %H:%M:%S")
count = 0;
if i<=50000:
	params = "{\"interfacename\":\"getserverinfo\",\"serverno\":\"1\"}" # urllib.urlencode(params)
	req = urllib2.Request(uri, params)    #����ҳ���������������
	#response = urllib2.urlopen(req)     #����ҳ������
	#print response.read()    #��ȡ���������ص�ҳ����Ϣ
	time.sleep(0.01)

	count += 1
	i+=1
	
print "���յ�%d�����"%count




def getcounterwaitpersons():
	params = "{\"interfacename\":\"getcounterwaitpersons\",\"counterno\":\"1\"}" # urllib.urlencode(params)
	req = urllib2.Request(uri, params)    #����ҳ���������������
	response = urllib2.urlopen(req)     #����ҳ������
	print response.read()    #��ȡ���������ص�ҳ����Ϣ

def counterlogin():
	# ���ڵ�¼�ӿ�
	params = "{\"interfacename\":\"counterlogin\",\"counterno\":\"1\",\"staffid\":\"1\",\"password\":\"\"}"
	req = urllib2.Request(uri, params)
	response = urllib2.urlopen(req)
	print response.read()

def counterlogin2():
	# ǩ�˽ӿ�
	params = "{\"interfacename\":\"counterunlogin\",\"counterno\":\"1\"}"
	req = urllib2.Request(uri, params)
	response = urllib2.urlopen(req)
	print response.read()


	# ��ȡ��һλ�ŶӺ���ӿ�
	params = "{\"interfacename\":\"getnextnumber\",\"counterno\":\"1\"}"
	req = urllib2.Request(uri, params)
	response = urllib2.urlopen(req)
	print response.read()

	# ��ȡ�Ⱥ������ӿ�
	params = "{\"interfacename\":\"getcounterwaitpersons\",\"counterno\":\"1\"}"
	req = urllib2.Request(uri, params)
	response = urllib2.urlopen(req)
	print response.read()

	# �����¼������ӿ�
	params = "{\"interfacename\":\"countereventaction\",\"counterno\":\"1\",\"staffid\":\"1\",\"serialid\":\"1\",\"transcodeid\":\"20160315092000-0001-A001\",\"eventid\":\"1\",\"number\":\"A001\"}"
	req = urllib2.Request(uri, params)
	response = urllib2.urlopen(req)
	print response.read()

	# �ŶӺ�ת��
	params = "{\"interfacename\":\"countertransfer\",\"counterno\":\"1\",\"transfertype\":\"1\",\"transcodeid\":\"20160315092000-0001-A001\",\"transfervalue\":\"1\",\"number\":\"A001\"}"
	req = urllib2.Request(uri, params)
	response = urllib2.urlopen(req)
	print response.read()

counterlogin();