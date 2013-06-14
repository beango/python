#-*- coding: UTF-8 -*-
#!/usr/bin/env python  
#coding:utf-8  
import time,json,random,re,hashlib
import XmlHelper,RequestHelper

class TieBa:
    __account = None
    __pwd = None
    
    def __init__(self):
        pass

    def login(self, account, pwd):
        self.__account = account
        self.__pwd = pwd
        """
            @url:https://passport.baidu.com/v2/api/?login
        """
        __headers ={
                'Pragma':'no-cache',\
                'Accept-Language':'zh-CN',\
                'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)'\
        }
        urlv = 'https://passport.baidu.com/v2/api/?login'
        _data={
            "callback": "parent.bdPass.api.login._postCallback",
            "charset": "utf-8",
            "codestring": "",
            "index": "0",
            "isPhone": "false",
            "loginType": "1",
            "mem_pass": "on",
            "password": self.__pwd,
            "ppui_logintime": "26166",
            "safeflg": "0",
            "staticpage": "http://www.baidu.com/cache/user/html/jump.html",
            "token": "9642aa11a26231e3926c4ee8a984a67c",
            "tpl": "mn",
            "u": "",
            "username": self.__account,
            "verifycode": ""
        }
        str = RequestHelper.request(url = urlv, cookies="", data=_data).encode('utf8')
        print str        
        pass

t = TieBa()
t.login("beango001", "adc1111")
