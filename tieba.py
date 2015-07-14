# -*- coding: utf-8 -*-  
# 2014.1.28 0:05 家里，坚持，便会柳暗花明。比别人笨无所谓，那就多花一点时间撒

import urllib, urllib2, cookielib, re, time
from bs4 import BeautifulSoup

baidu_url = 'http://www.baidu.com/'         #为获取cookie，具体不懂
token_url = 'https://passport.baidu.com/v2/api/?getapi&tpl=pp&apiver=v3&class=login'  #此链接可获取token，网址怎么分析出来的，不理解
login_url = 'https://passport.baidu.com/v2/api/?login'      #post网址，1E F12分析
like_url = 'http://tieba.baidu.com/f/like/mylike?&pn='      #怎么分析出来的
sign_url = 'http://tieba.baidu.com/sign/add'                #post
# 自动保存cookie  整个程序内都有效还是？

def welcome_():
    #print '-'*40
    #print u'\n'
    return
    
def cookie_():
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    urllib2.urlopen(baidu_url)
    
def token_():
    content = urllib2.urlopen(token_url).read()
    token = re.findall('"token" : "(.*?)"',content)[0]
    print 'token: ',token
    return token
    
def login_(name,pwd):
    while True:
        """
        name = raw_input(u'请输入用户名，按回车键结束:'.encode('gbk'))
        pwd = raw_input(u'请输入密码:，按回车键结束:'.encode('gbk'))
        """
        # 必要的表单数据，是慢慢筛出来的-->
        postdata = {
                'staticpage':'https://passport.baidu.com/static/passpc-account/html/v3Jump.html',
                #'charset':'UTF-8',
                'token':token,
                'tpl':'pp',
                'apiver':'v3',
                'isPhone':'false',
                'username':name,
                'rsakey':'w2WVAgLod8IyPX97ovmKmNCP1XmEjabW',
                'password':'oBIooKInQAOYtQI5m5tVkqKVz0jXjjoIh3Z5Rer/FmaqPIr8nB9An1e/Qh+oBdQDVZRjSAoOoOYkqPZ/9oSm0cy8pm48s45v9QXlHwy6Sa6iujWpD22tPpWX9BwjojRCL5EIFCFlMg+tl+y248yLij96mE2l8p89C/5CYuOwSr0=',
                #'callback':'parent.bd__pcbs__poaxot',
                #'u':'https://passport.baidu.com/'
                }
        postdata = urllib.urlencode(postdata)
        req = urllib2.Request(login_url,postdata)
        sendpost = urllib2.urlopen(req)
        response = urllib2.urlopen('http://passport.baidu.com/center')
        print response.info().getheader('Content-Type')
        center = response.read()
        print center;
        if re.findall('百度帐号登录',center)==[]:
            content = urllib2.urlopen('http://passport.baidu.com/center').read()
            open('1.txt','wb').write(content)
            print '登录成功'+'-'*20
            break
        else:
            s = u'登录失败，请检查用户名和密码'
            width = (80-len(s)*2)/2
            print ' '*width+s
            time.sleep(1)
            (name,pwd) = account.account()
        ##############################################加入登录是否成功的测试
        # 测试是否登录成功
        
    
def sign_():
    print '开始签到'+'-'*20
    i = 1
    while True:
        opener = urllib2.build_opener()
        opener.addheaders.append(('Cookie', 'BAIDUID=2D0F4B3872C88C06730E884002C73ADC:FG=1; TIEBA_USERTYPE=3b1b6fd72b655ca34a971e97; TIEBAUID=2efb27f7f5cf5e1138f3e5ea; bdshare_firstime=1433144412282; rpln_guide=1; BIDUPSID=2D0F4B3872C88C06730E884002C73ADC; PSTM=1433387013; GET_TOPIC=793371913; showCardBeforeSign=1; baidu_broswer_setup_________å§ä¸¶æ®=0; BDRCVFR[08EbrmKd5E_]=aeXf-1x8UdYcs; H_PS_PSSID=14767_1434_13349_14511_14444_12867_14622_14669_12723_14625_14484_12427_10633; BDUSS=dndG5rVDlXTVZyRHlkZlVNOUpRWE94amQ5dDlGOUtUcWpPMnpDUXhqdzd2S1ZWQVFBQUFBJCQAAAAAAAAAAAEAAAAJ5UkvX19fX19fX1-H5di86eQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADsvflU7L35VQz; wise_device=0; Hm_lvt_287705c8d9e2073d13275b18dbd746dc=1433993643,1434073932,1434331059,1434335187; Hm_lpvt_287705c8d9e2073d13275b18dbd746dc=1434335402'))
        like_content = opener.open(like_url+str(i)).read()

        soup =BeautifulSoup(like_content)
        print soup
        for a in soup.find_all('a',href=True,title=True,class_=False):
            name = a.string   # 貌似BS的内容全为unicode
            href = a.get('href')
            print name.encode('utf8')+'吧，签到成功'
            tieba_url = 'http://tieba.baidu.com'+href
            tbs = re.findall('PageData.tbs = "(.*?)"',urllib2.urlopen(tieba_url).read())[0]
            #print tbs
            postdata = {
                        'ie':'utf-8',
                        'kw':name.encode('utf8'),       # 因为BS的内容为unicode
                        'tbs':tbs
                        }
            postdata = urllib.urlencode(postdata)
            req = urllib2.Request(sign_url,postdata)
            urllib2.urlopen(req)
        print '-'*40
        #print content
        
        if re.findall('<td>',like_content) == []:
            print '全部贴吧签到完毕，输入任意键退出程序'
            a = raw_input('>-')
            break
        i+=1

        
welcome_()
cookie_()
token = token_()
login_('6588617@qq.com','zxc12345')
sign_()