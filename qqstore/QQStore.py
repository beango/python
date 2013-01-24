#-*- coding: UTF-8 -*-
#!/usr/bin/env python  
#coding:utf-8  
import time,json,random,re,hashlib
import XmlHelper,RequestHelper

class QQ:
    """
     Login QQ
    """
    __qq = None
    __pswd = None
    __clientid = 21628014
    __psessionid = ''
    __ptwebqq = ''
    __vfwebqq = ''
    __skey = ''
    __poll2 = None
    __get_msg_tip = None
    __rc = 0
    __send_num = 31330000
    __gtk = None
    __username = None
    __seckey = None
    verifycode = None
    uin = None
    
    def __init__(self, qq, pswd):
        self.__frametime = "%s" % int(time.time())
        self.__qq = qq
        self.__pswd = pswd
        pass

    def getframekey1(self):
        frametime = self.__frametime
        key = "OPdfqwn^&*w(281flebnd1##roplaq"
        str = key[int(frametime[-1:]):]
        m = hashlib.md5()
        m.update(frametime + str)
        return m.hexdigest()

    def getframekey2(self,frametime):
        key = "LOL#ahri%zyra^Brand@101i$Ele)+"
        str = key[int(frametime[-1:]):]
        m = hashlib.md5()
        m.update(frametime + str)
        return m.hexdigest()

    def getg_tk(self, skey):
        hash = 5381
        for i in skey:
            hash += (hash << 5) + ord(i)
        return hash & 0x7fffffff;

    def getlv(self, exp):#计算农场等级
        lv = 1
        while (lv+2)*(lv+1)*100 <= exp and lv<1000:
            lv+=1;
        return [lv,exp-(lv*(lv+1)*100)]

    def md5_hex(self, s):
        m = hashlib.md5()
        m.update(s)
        return m.hexdigest()
        pass

    def md5_bin(self, s):
        m = hashlib.md5()
        m.update(s)
        return m.digest()
        pass

    def encypt_password2(self):
        r = self.md5_bin(self.__pswd) + self.uin
        r = self.md5_hex(r)
        r = (r + self.verifycode).upper()
        r = self.md5_hex(r).upper()
        return r
        pass

    def getverifycode(self):
        """
            @url:http://check.ptlogin2.qq.com/check?uin=147841329&appid=15000101&ptlang=2052&r=0.6747
        """
        __headers ={
                'Pragma':'no-cache',\
                'Accept-Language':'zh-CN',\
                'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)'\
        }
        urlv = 'http://check.ptlogin2.qq.com/check?uin='+ "%s"%self.__qq +'&appid=15000101&ptlang=2052&r='+ ('%s' % random.Random().random())
        #cookiestr = self.initcookie()
        str = RequestHelper.request(url = urlv, savecookie=True, cookies="").encode('utf8')
        print str

        chunk = re.match("ptui_checkVC\(\'(\d+)\',\'(.*)\',\'(.*)\'\)",str);
        self.uin = bytearray.fromhex(chunk.group(3).replace("\\x",""))

        if int(chunk.group(1)) == 0:
            open("code.txt","w").write(chunk.group(2))
        else:
            url = "http://captcha.qq.com/getimage?aid=15000101&r=0.45623475915069394&uin=" + "%s"%self.__qq
            str = self.request(url = url, savecookie=True, cookies=self.initcookie()).encode('utf8')
            vc = open("vc.jpg","wb").write(str)

            fname = "vc.jpg"
            opener = urllib.urlopen(url)
            open(fname, 'wb').write(opener.read())
        pass

    def login(self):
        '''
        http://ptlogin2.qq.com/login?ptlang=2052&u=6588617&p=&verifycode=!4BN&css=http://imgcache.qq.com/ptcss/b2/qzone/15000101/style.css&mibao_css=m_qzone&aid=15000101&u1=http%3A%2F%2Fimgcache.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone&ptredirect=1&h=1&from_ui=1&dumy=&fp=loginerroralert&action=7-24-19703&g=1&t=1&dummy=
        '''
        __headers ={
                'Pragma':'no-cache',\
                'Accept-Language':'zh-CN',\
                'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)'\
        }
        url = "http://ptlogin2.qq.com/login?ptlang=2052&u="+"%s"%self.__qq+"&p="+"%s"%self.uin+"&verifycode="+self.verifycode + \
              "&css=http://imgcache.qq.com/ptcss/b2/qzone/15000101/style.css&mibao_css=m_qzone&aid=15000101&u1=http%3A%2F%2Fimgcache.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone&ptredirect=1&h=1&from_ui=1&dumy=&fp=loginerroralert&action=7-24-19703&g=1&t=1&dummy="#登录验证码

        cookies = ["confirmuin","ptisp","ptvfsession"]
        str = RequestHelper.request(url = url, savecookie=True, cookies=cookies).encode('utf8')
        '''
        ptuiCB('7','0','','0','很遗憾，网络连接出现异常，请您稍后再试。(298848060)', '147841329');
        '''
        chunk = re.match("ptuiCB\(\'(\d+)\',\'(\d+)\',\'(.*)\',\'(\d+)\',\'(.[^']*)\',.*\'(.[^']*)\'\);",str);
        self.__username = chunk.group(6)
        return chunk.group(5) == '登录成功！'

    def step1(self):
        '''
        http://appframe.qq.com/cgi-bin/qzapps/appframe.cgi?q_ver=6&pf=qzone&appid=21641&g_tk=804536038
        Cookie: pt2gguin=o0147841329; uin=o0147841329; skey=@zj93WmOvH; ETK=; ptisp=ctc; RK=abSGJjXKUM; ptuserinfo=313437383431333239; 
        ptcz=a9314965f215d012fe5fe2dc6cda2004d72b918867c1670fe3c84a1a09284c98; airkey=;
        Referer: http://user.qzone.qq.com/147841329/infocenter
        '''
        headers ={
                'Pragma':'no-cache',\
                'Accept-Language':'zh-CN',\
                'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)',\
                'Referer':'http://user.qzone.qq.com/'+'%s'%self.__qq+'/infocenter'\
        }
        cookies = ["pt2gguin","uin","skey","ETK","ptisp","RK","ptuserinfo","ptcz","airkey"]
        self.__gtk = self.getg_tk(RequestHelper.getcookie("skey"))

        url = "http://appframe.qq.com/cgi-bin/qzapps/appframe.cgi?q_ver=6&pf=qzone&appid=21641&g_tk=" + "%s"%self.__gtk
        
        str = RequestHelper.request(url = url, savecookie=True, cookies=cookies, header=headers).encode('utf8')
        
    def step2(self):
        '''
        /?qz_height=900&qz_width=950&openid=0000000000000000000000000BF740B1&openkey=9519618DA0AF947877BDBC71340E99FF424F8F252E9F7B336B3C948517CA059A70DB4243A735D89587094BC1641A18DF570E5190D088508A5F4A65797F1320639DBE8F6CABCD2B7D925D0FFCA7BD5ECD41B47FC9814796F9&pfkey=898b3a6e21d523afd6e517eee0f69b27&pf=qzone&qz_ver=6&appcanvas=1&params=&via=QZ.MYAPP
        Cookie: pt2gguin=o0147841329; uin=o0147841329; skey=@zj93WmOvH; ETK=; ptisp=ctc; RK=abSGJjXKUM; 
        ptuserinfo=313437383431333239; ptcz=a9314965f215d012fe5fe2dc6cda2004d72b918867c1670fe3c84a1a09284c98; airkey=;
        '''
        headers ={
                'Pragma':'no-cache',\
                'Accept-Language':'zh-CN',\
                'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)',\
                'Referer':'http://user.qzone.qq.com/'+'%s'%self.__qq+'/infocenter'\
        }
        cookies = ["pt2gguin","uin","skey","ETK","ptisp","RK","ptuserinfo","ptcz","airkey"]
        self.__gtk = self.getg_tk(RequestHelper.getcookie("skey"))

        url = "http://app21641.qzone.qzoneapp.com/?qz_height=900&qz_width=950&openid=0000000000000000000000000BF740B1&openkey=9519618DA0AF947877BDBC71340E99FF424F8F252E9F7B336B3C948517CA059A70DB4243A735D89587094BC1641A18DF570E5190D088508A5F4A65797F1320639DBE8F6CABCD2B7D925D0FFCA7BD5ECD41B47FC9814796F9&pfkey=898b3a6e21d523afd6e517eee0f69b27&pf=qzone&qz_ver=6&appcanvas=1&params=&via=QZ.MYAPP"
        
        str = RequestHelper.request(url = url, savecookie=True, cookies=cookies, header=headers).encode('utf8')
     
    def step3(self):
        '''
        /?qz_height=900&qz_width=950&openid=0000000000000000000000000BF740B1&openkey=9519618DA0AF947877BDBC71340E99FF424F8F252E9F7B336B3C948517CA059A70DB4243A735D89587094BC1641A18DF570E5190D088508A5F4A65797F1320639DBE8F6CABCD2B7D925D0FFCA7BD5ECD41B47FC9814796F9&pfkey=898b3a6e21d523afd6e517eee0f69b27&pf=qzone&qz_ver=6&appcanvas=1&params=&via=QZ.MYAPP
        Cookie: pt2gguin=o0147841329; uin=o0147841329; skey=@zj93WmOvH; ETK=; ptisp=ctc; RK=abSGJjXKUM; 
        ptuserinfo=313437383431333239; ptcz=a9314965f215d012fe5fe2dc6cda2004d72b918867c1670fe3c84a1a09284c98; airkey=;
        '''
        headers ={
                'Pragma':'no-cache',\
                'Accept-Language':'zh-CN',\
                'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)',\
                'Referer':'http://user.qzone.qq.com/'+'%s'%self.__qq+'/infocenter'\
        }
        cookies = ["pt2gguin","uin","skey","ETK","ptisp","RK","ptuserinfo","ptcz","airkey"]
        self.__gtk = self.getg_tk(RequestHelper.getcookie("skey"))

        url = "http://openplat.gamesafe.qq.com/cgi-bin/sec.fcgi?req=status&jsonp=SecJs.status_rsp&appid=21641&rn=0.683474951190874"
        
        str = RequestHelper.request(url = url, savecookie=True, cookies=cookies, header=headers).encode('utf8')
        chunk = re.match("SecJs.status_rsp\((.*)\);",str);
        self.__seckey = json.loads(chunk.group(1))["seckey"]
        print self.__seckey

    def step4(self):
        '''
        /cgi-bin/feeds/cgi_get_feeds_count.cgi?uin=6588617&lockese=0.446679925313219&g_tk=1633614837
        '''
        headers ={
                'Pragma':'no-cache',\
                'Accept-Language':'zh-CN',\
                'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)',\
                'Referer':'http://user.qzone.qq.com/'+'%s'%self.__qq+'/infocenter'\
        }
        RequestHelper.addcookies(["ptui_qstatus=2"])
        cookies = ["uin","skey","ETK","ptisp","RK","pt2gguin"]
        self.__gtk = self.getg_tk(RequestHelper.getcookie("skey"))

        url = "http://ic2.s11.qzone.qq.com/cgi-bin/feeds/cgi_get_feeds_count.cgi?uin="+ "%s"%self.__qq +"&lockese=0.446679925313219&g_tk=" + "%s"%self.__gtk
        
        str = RequestHelper.request(url = url, savecookie=True, cookies=cookies, header=headers).encode('utf8')
        print "step4:"+str
    
    def step5(self):
        '''
        /cgi-bin/feeds/cgi_get_feeds_count.cgi?uin=6588617&lockese=0.446679925313219&g_tk=1633614837
        '''
        headers ={
                'Pragma':'no-cache',\
                'Accept-Language':'zh-CN',\
                'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)',\
                'Referer':'http://user.qzone.qq.com/'+'%s'%self.__qq+'/infocenter'\
        }
        RequestHelper.addcookies(["ptui_qstatus=2"])
        cookies = ["uin","skey","ETK","ptisp","RK","pt2gguin"]
        self.__gtk = self.getg_tk(RequestHelper.getcookie("skey"))

        url = "http://openplat.gamesafe.qq.com/cgi-bin/sec.fcgi?req=status&jsonp=SecJs.status_rsp&seckey="+self.__seckey+"&appid=21641&rn=0.0848684282973409"
        print url
        str = RequestHelper.request(url = url, savecookie=True, cookies=cookies, header=headers).encode('utf8')
        print str

def Login(qq, pwd):
    """
        qq登录
    """
    open("console.txt","w").close()
    q = QQ(qq, pwd)
    q.getverifycode()
    while q.verifycode == None or len(q.verifycode) != 4:
        time.sleep(1)
        f = open("code.txt")
        q.verifycode = f.read()
        f.close()
    q.uin = q.encypt_password2()
    open("code.txt","w").close()
    if q.login():
        q.step1()
        q.step2()
        q.step3()
        q.step4()
        q.step5()
    else:
        print '登录失败'

            
Login(147841329,"3622041982")
