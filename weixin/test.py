#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import httplib, sys, urllib, time
from xml.dom import minidom
from loadfeed import loadfeed

httpClient = None

def request_hello():
    try:
        httpClient = httplib.HTTPConnection('localhost', 8080, timeout=10)
        httpClient.request('GET', '/hello?accmy=gobing')

		# response是HTTPResponse对象
        response = httpClient.getresponse()
        print response.status
        print response.reason
        print response.read()
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()

def request():
	try:
		httpClient = httplib.HTTPConnection('localhost', 8080, timeout=10)
		httpClient.request('GET', '/weixin?echostr=123&signature=222&timestamp=012&nonce=po')

		# response是HTTPResponse对象
		response = httpClient.getresponse()
		print response.status
		print response.reason
		print response.read()
	except Exception, e:
		print e
	finally:
		if httpClient:
			httpClient.close()
def post():
	try:
		params = '<xml><URL><![CDATA[http://45.78.23.29/weixin]]></URL><ToUserName><![CDATA[beango2015]]></ToUserName><FromUserName><![CDATA[oOjVGwaH52NRcPYOyESY7PCb1VRw]]></FromUserName><CreateTime>123</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[?1]]></Content><MsgId>11123</MsgId></xml>'#urllib.urlencode({'nonce': u'929260242', 'timestamp': u'1475910692', 'openid': u'o2WRzv6YXhs8nw4y34CXeiAyFa9w', 'signature': u'3f7293922743f8569f436660b5b2d8dff273bf4c'})
		headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
		httpClient = httplib.HTTPConnection('localhost', 8080, timeout=10)
		httpClient.request('POST', '/weixin?nonce=929260242&timestamp=1475910692&openid=o2WRzv6YXhs8nw4y34CXeiAyFa9w&signature=3f7293922743f8569f436660b5b2d8dff273bf4c', params, headers)
		response = httpClient.getresponse()
		print response.status
		print response.reason
		print response.read()
		print response.getheaders()
	except Exception, e:
		print e
	finally:
		if httpClient:
			httpClient.close()

'''
Sat, 08 Oct 2016 21:58:44 app.py[line:60] INFO <Storage {'nonce': u'854805214', 'openid': u'o2WRzv6YXhs8nw4y34CXeiAyFa9w', 'timestamp': u'1475978323', 'encrypt_type': u'aes', 'signature': u'bd5a92a4bb5ac753d9e1fef7c9077ccd403deb5d', 'msg_signature': u'f2e693e9aed5c7b85e1b6e567931ec8892cd6502'}>
Sat, 08 Oct 2016 21:58:44 app.py[line:61] INFO <xml>
    <ToUserName><![CDATA[gh_6560647450fd]]></ToUserName>
    <Encrypt><![CDATA[8mohVIh8X9ck60bEMFItoGyY5kfEnbBZPPPmtXVcfNbpjY9q9T/P/eKbNkF3AUon1sRSnTfESK6FpbssrM5S3wP6WgQytJCtv9NXaUXxePUib0pX3dWo/DKSSybGa6GmN8Ri+HYwYbYReRD+WA7jaR4V9hRO/pzCV15Xvf6qqcDq9WXV+mOVO2y0Tm0WmOenhC2TtrCHxm/faBy0ZqKCtGeRZb2hYRZ48tDHG2VjrMBelQ2ec5clrZm5ofzNwKLnzNa0BR84u4tkRvuCWARKcxqG6Vhmqeb+Eyf++6RoJr3sXOtB/U/tR4xw/bL4USvb3uWgBMglB4XW9vArmsMaZMhy9Q0DcQ+M0/yEx91XTHuSDPpe1Rb25wcT1Dh2+dWO311PZWZuuUEPYM5X+s9twvqe2QckwXLbWoZfrhiZ/cA=]]></Encrypt>
</xml>
'''
def post_encrypt():
	try:
		params = """<xml>
    <ToUserName><![CDATA[gh_6560647450fd]]></ToUserName>
    <Encrypt><![CDATA[8mohVIh8X9ck60bEMFItoGyY5kfEnbBZPPPmtXVcfNbpjY9q9T/P/eKbNkF3AUon1sRSnTfESK6FpbssrM5S3wP6WgQytJCtv9NXaUXxePUib0pX3dWo/DKSSybGa6GmN8Ri+HYwYbYReRD+WA7jaR4V9hRO/pzCV15Xvf6qqcDq9WXV+mOVO2y0Tm0WmOenhC2TtrCHxm/faBy0ZqKCtGeRZb2hYRZ48tDHG2VjrMBelQ2ec5clrZm5ofzNwKLnzNa0BR84u4tkRvuCWARKcxqG6Vhmqeb+Eyf++6RoJr3sXOtB/U/tR4xw/bL4USvb3uWgBMglB4XW9vArmsMaZMhy9Q0DcQ+M0/yEx91XTHuSDPpe1Rb25wcT1Dh2+dWO311PZWZuuUEPYM5X+s9twvqe2QckwXLbWoZfrhiZ/cA=]]></Encrypt>
</xml>"""
		headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
		httpClient = httplib.HTTPConnection('localhost', 8080, timeout=10)
		httpClient.request('POST', '/weixin?encrypt_type=aes&msg_signature=f2e693e9aed5c7b85e1b6e567931ec8892cd6502&nonce=854805214&timestamp=1475978323&openid=o2WRzv6YXhs8nw4y34CXeiAyFa9w&signature=bd5a92a4bb5ac753d9e1fef7c9077ccd403deb5d', params, headers)
		response = httpClient.getresponse()
		print response.status
		print response.reason
		#print response.read()
	except Exception, e:
		print e
	finally:
		if httpClient:
			httpClient.close()

print time.strftime("%Y-%m-%d %H:%M:%S")
post_encrypt()
