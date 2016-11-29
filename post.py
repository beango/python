#!/usr/bin/python
#coding=utf-8
 
import urllib,urllib2
 
uri = 'http://localhost:8082/queueSysinterface.aspx'
params = {
'_c': 'user',
'_m': 'info',
};
 
params['interfacename']	= 'getlcddeviceprams'
params['devicemac'] = '080027D1E824'
params = urllib.urlencode(params)
ret = urllib.urlopen(uri, params)
code = ret.getcode()
ret_data = ret.read()

print ret_data
