#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# Author: jonyqin
# Created Time: Thu 11 Sep 2014 03:55:41 PM CST
# File Name: demo.py
# Description: WXBizMsgCrypt 使用demo文件
#########################################################################
from WXBizMsgCrypt import WXBizMsgCrypt
if __name__ == "__main__":   
   """ 
   1.第三方回复加密消息给公众平台；
   2.第三方收到公众平台发送的消息，验证消息的安全性，并对消息进行解密。
   """
   encodingAESKey = "2JNBFX4wjJmHY5EHfvWG0ZzYzMUQJrHu4T3u5sO8ZHz" 
   to_xml = """<xml>
    <ToUserName><![CDATA[o2WRzv6YXhs8nw4y34CXeiAyFa9w]]></ToUserName>
    <FromUserName><![CDATA[gh_6560647450fd]]></FromUserName>
    <CreateTime>1475979506</CreateTime>
    <MsgType><![CDATA[news]]></MsgType>
    <ArticleCount>3</ArticleCount>
    <Articles>
    
    <item>
        <Title><![CDATA[中文玉Nginx]]></Title>
        <Description><![CDATA[]]></Description>
        <PicUrl><![CDATA[images]]></PicUrl>
        <Url><![CDATA[http://uwebs.tk/archives/2015/06/15/12-nginx-performance-tuning.html]]></Url>
    </item>
    
    <item>
        <Title><![CDATA[Shell鑴氭湰缂栫▼鍒濅綋楠宂]></Title>
        <Description><![CDATA[]]></Description>
        <PicUrl><![CDATA[images]]></PicUrl>
        <Url><![CDATA[http://uwebs.tk/archives/2015/06/10/guide-start-learning-shell-scripting-scratch.html]]></Url>
    </item>
    
    <item>
        <Title><![CDATA[python realtime]]></Title>
        <Description><![CDATA[]]></Description>
        <PicUrl><![CDATA[images]]></PicUrl>
        <Url><![CDATA[http://uwebs.tk/archives/2014/08/05/python-realtime.html]]></Url>
    </item>
    
    </Articles>
    </xml>"""
   token = "doumitest"
   nonce = "1545799455"
   appid = "wx3386db73536a091d"
   #测试加密接口
   encryp_test = WXBizMsgCrypt(token,encodingAESKey,appid)
   ret,encrypt_xml = encryp_test.EncryptMsg(to_xml,nonce)   
   print ret,encrypt_xml 
   

   #测试解密接口
   timestamp = "1475977746"
   msg_sign  = "7f0faa4bcb46a7621a933e459f014d421a3e8322"   
   
   from_xml = """<xml>
    <ToUserName><![CDATA[gh_6560647450fd]]></ToUserName>
    <Encrypt><![CDATA[XDWc0SlTYmw7KTbHK3awfPzl6K2Dhdr39opyb1UKeP3KyCHxmSHtC0S5e7OpMTeXRFMh1HfRMki8xBEAW7RD2LzKrvpMvT3DwVXQ/DCSalHvhciD+6Hi5aRthSUAioT9N9/wh7WM7mjtj95K7NDmgdB6h3WW7SV5fBENotcqOWy0yNUPK0D2o+cjfSmdiSAF3A1js1HkGbmDnlKOXsBt/aocV6bVbF/2N7uIwTkXM9K0IZnBDKwUg7oAlP6B8wRlUP5RefVB20LywDfPre/7A/b3DWkqA+frfOGiUkKAmLlI0gIgnTlriBF14m5oX7TNTOyjdW7pz5nzBLBgIl1d9zhL0eZgXq+lyqhQa3DuCxs7F5H+6/NDJzApFhVJ7X8gRpefGFfJpxnXV4HbqBvFIUCSPOrkM6H6EG8JTzRlSxc=]]></Encrypt>
</xml>
"""
   decrypt_test = WXBizMsgCrypt(token,encodingAESKey,appid)
   ret ,decryp_xml = decrypt_test.DecryptMsg(from_xml, msg_sign, timestamp, nonce)
   print ret ,decryp_xml
