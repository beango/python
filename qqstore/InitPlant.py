#-*- coding: UTF-8 -*-
#!/usr/bin/env python  
#coding:utf-8  
import RequestHelper
import urllib2
"""""""""""""""""""""""""""""""""""""""
获取农场作物信息，包含等级，成熟时间
"""""""""""""""""""""""""""""""""""""""

class InitPlant:
    def Get_Frame_Data(self):
        headers ={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding': 'gzip,deflate,sdch',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11'
        }

        url = "http://ctc.appimg.qq.com/happyfarm/data/data_zh_CN_v_411.xml"
        cookies = ["luin","lskey","ptui_loginuin","pt2gguin","__hash__","pgv_pvi"," pgv_pvid"," o_cookie"]
        
        data=RequestHelper.request(url).encode("utf8")
        open("Data/frame_data.xml","w").write(data)
        pass

if __name__ == "__main__":
    InitPlant().Get_Frame_Data()
        