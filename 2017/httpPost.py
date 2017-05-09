# -*- coding:utf-8 -*-  

import urllib
import urllib2
url = 'http://112.74.208.56:8080/DeviceManage/manage/DmCheck/checkDevice.htm'
values = {'deviceno':'20170331101721','comments':'可以呀','checkrst':1,'commitUser':1}
data = urllib.urlencode(values)
print data
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
the_page = response.read()
print the_page

