#-*- coding: UTF-8 -*-
#!/usr/bin/env python  
#coding:utf-8  
import urllib,urllib2,cookielib

"""""""""""""""""""""""""""""""""""""""
request辅助类
"""""""""""""""""""""""""""""""""""""""

class RequestHelper:
    __headers ={
                'Pragma':'no-cache',
                'Accept-Language':'zh-CN',
                'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)'
    }
    __cookiepath = 'Data/cookies.txt'
    __cookielist = []
    __http = {}

    def __init__(self):
        self.httpproess()
        pass

    def httpproess(self):
        """
        初始化模拟进程
        """
        self.__http['cj'] = cookielib.MozillaCookieJar(self.__cookiepath)
        self.__http['opener'] = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.__http['cj']))
        try:
            self.__http['cj'].load(ignore_discard=True, ignore_expires=True)
        except:
            self.__http['cj'] = []
        return self.__http
        pass   
        
    def addcookies(self,cookies=[]):
        self.__cookielist.extend(cookies)
        
    def request(self, url, method='GET', header = None, data={},savecookie=False,cookies=[]):
        """
        请求url
        """
        if header != None:
            self.__headers = header
        if (method).upper() == 'POST':
            data = urllib.urlencode(data)
            req = urllib2.Request(url,data,headers=self.__headers)
        else:
            req = urllib2.Request(url,headers=self.__headers)
        if len(cookies)>0:
            self.__cookielist.extend([" "+c.name+"="+c.value for c in self.__http['cj'] if c.name in cookies])
            self.__cookielist.extend([" "+c+"=" for c in cookies if c not in [i.name for i in self.__http['cj']]])
            cookiestr = ";".join(self.__cookielist)
            req.add_header("Cookie",cookiestr)
        fp = self.__http['opener'].open(req)

        try:
            str = fp.read().decode('utf8')
        except UnicodeDecodeError:
            str = fp.read()

        if savecookie:
            self.__http['cj'].save(ignore_discard=True, ignore_expires=True)
        fp.close()
        return str
        pass
    
    def open(self, url):
        response = urllib2.urlopen(url);
        print type(response.read())
        return response.read()

    def getcookie(self, name):
        for ck in self.__http['cj']:
            if ck.name==name:
                return ck.value

def request(url,method='GET',header=None,data={},savecookie=False,cookies=[]):
    h = RequestHelper()
    return h.request(url, method,header, data, savecookie, cookies)

def open(url):
    h = RequestHelper()
    return h.open(url)

def getcookie(name):
    h = RequestHelper()
    return h.getcookie(name)

def addcookies(cookies=[]):
    h = RequestHelper()
    h.addcookies(cookies)
