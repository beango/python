#!/usr/bin/python2.7 
# -*- coding: utf-8 -*- 
import requests
import json
import urllib
import hashlib
import sys,time,random
from datetime import datetime
import ssl

#ssl._create_default_https_context = ssl._create_unverified_context

inte = 'http://localhost:8081/queueInterface'
headers={'UserAgent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)', 'Content-Type': 'application/json', 'Content-Encoding': 'gzip'}
client_cert_key = "etcd-client-key.pem" # file path
client_cert_pem = "etcd-client.pem"     # file path 
ca_certs = "etcd-ca.pem"                # file path

def logins():
    CA_FILE = "/work/workspace/ZX/zxcall/go/cert/server.crt"

    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.check_hostname = False
    context.load_verify_locations(CA_FILE)
    context.verify_mode = ssl.CERT_REQUIRED
    try:
        
        values={"interfacename": "counterlogin", "counterno":"1", "staffid":"1", "password":"1"}
        request = urllib.request.Request(inte, headers = headers, data = json.dumps(values).encode('utf-8'))
        res = urllib.request.urlopen(request, context=context)
        print(res.code)
        print(res.read().decode("utf-8"))
    except Exception as ex:
        print("Found Error in auth phase:%s" % str(ex))

    # handlers.append(https.HTTPSClientAuthHandler( 
    #     key = client_cert_key,
    #     cert = client_cert_pem,
    #     ca_certs = ca_certs,
    #     ssl_version = ssl.PROTOCOL_SSLv23,
    #     ciphers = 'TLS_RSA_WITH_AES_256_CBC_SHA' ) )

    # http = urllib2.build_opener(*handlers)
    # values={"interfacename": "counterlogin", "counterno":"1", "staffid":"1", "password":"1"}
    # request=urllib2.Request(url=inte, headers=headers, data=json.dumps(values))
    # params = json.dumps(values)
    # response=urllib2.urlopen(request)

    # print (response.read())

def login():
    try:
        values={"interfacename": "counterlogin", "counterno":"1", "staffid":"1", "password":"1"}
        request = urllib.request.Request(inte, headers = headers, data = json.dumps(values).encode('utf-8'))
        res = urllib.request.urlopen(request)
        print(res.code)
        print(res.read().decode("utf-8"))
    except Exception as ex:
        print("Found Error in auth phase:%s" % str(ex))

def logout():
    try:
        values={"interfacename": "counterlogout", "counterno":"1", "staffid":"1", "password":"1"}
        request = urllib.request.Request(inte, headers = headers, data = json.dumps(values).encode('utf-8'))
        res = urllib.request.urlopen(request)
        print(res.code)
        print(res.read().decode("utf-8"))
    except Exception as ex:
        print("Found Error in auth phase:%s" % str(ex))

def welcome():
    try:
        values={"interfacename": "countereventaction", "counterno":"1", "staffid":"1", "staffname":"服务员1","eventid":"8"}
        request = urllib.request.Request(inte, headers = headers, data = json.dumps(values).encode('utf-8'))
        res = urllib.request.urlopen(request)
        print(res.code)
        print(res.read().decode("utf-8"))
    except Exception as ex:
        print("Found Error in auth phase:%s" % str(ex))

def service():
    try:
        values={"interfacename": "countereventaction", "counterno":"1", "staffid":"1", "staffname":"服务员1","eventid":"2", "transcodeid": "0-0000-1-20200408153847-A008"}
        request = urllib.request.Request(inte, headers = headers, data = json.dumps(values).encode('utf-8'))
        res = urllib.request.urlopen(request)
        print(res.code)
        print(res.read().decode("utf-8"))
    except Exception as ex:
        print("Found Error in auth phase:%s" % str(ex))


def getnextnum():
    try:
        values={"interfacename": "getnextnumber", "counterno":"1", "staffid":"1", "staffname":"服务员1","eventid":"2", "transcodeid": "1111"}
        request = urllib.request.Request(inte, headers = headers, data = json.dumps(values).encode('utf-8'))
        res = urllib.request.urlopen(request)
        print(res.code)
        print(res.read().decode("utf-8"))
    except Exception as ex:
        print("Found Error in auth phase:%s" % str(ex))

welcome()
