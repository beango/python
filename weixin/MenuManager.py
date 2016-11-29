#!/usr/bin/env python
# -*- coding: utf-8 -*
'''
'''
import urllib2
import json, sys
reload(sys)
sys.setdefaultencoding('utf-8')
 
class MenuManager:
    AppID = 'wx29d037350215aa48' #测试号 wx29d037350215aa48
    AppSecret = '4a8de503bfe20c865753f6c971268dfc' #测试号 4a8de503bfe20c865753f6c971268dfc
    accessUrl = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" %(AppID, AppSecret)
    delMenuUrl = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token="
    createUrl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token="
    getMenuUri="https://api.weixin.qq.com/cgi-bin/menu/get?access_token="
    def getAccessToken(self):
        getTokenResult = urllib2.urlopen(self.accessUrl)
        print self.accessUrl
        tokenJson = json.loads(getTokenResult.read())
        token = tokenJson['access_token']
        print token
        return token 

    def delMenu(self, accessToken):
        html = urllib.request.urlopen(self.delMenuUrl + accessToken)
        result = json.loads(html.read().decode("utf-8"))
        return result["errcode"]
    def createMenu(self, accessToken):
        menu = '''{
        "button":[{
            "name":"这不是空",
            "sub_button":[
                {"type":"view","name":"测试１","url":"http://uwebs.tk"}
            ]
        },
        {    
            "type":"click",
            "name":"空的",
            "key":"V1001_HELLO_WORLD"
        },
        {
            "name":"菜单",
            "sub_button":[
                {"type":"view","name":"GitHub","url":"http://www.github.com/beango"},
                {"type":"view","name":"我的主页","url":"http://uwebs.tk"}
            ]
        }]}'''

        param = json.loads(menu)
        data = json.dumps(param, ensure_ascii=False, encoding='utf-8').encode('utf-8')
        req = urllib2.Request(self.createUrl + accessToken, data)
        response = urllib2.urlopen(req)
        print response.read()

    def getMenu(self, accessToken):
        req = urllib2.Request(self.getMenuUri + accessToken)
        content = urllib2.urlopen(req).read() #json格式数据
        print content.decode("utf-8")
        #menuDict = json.loads(getMenuResult.read())
        #menu = json.dumps(menuDict, ensure_ascii=False, encoding='utf-8').encode('utf-8')
     
 
if __name__ == "__main__":
    wx = MenuManager()
    accessToken = wx.getAccessToken()
    #print(wx.delMenu(accessToken))   #删除菜单
    wx.createMenu(accessToken)  #创建菜单
    wx.getMenu(accessToken)