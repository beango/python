#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import web, hashlib, re, urllib2, json
import xml.etree.ElementTree as ET
import logging, time
from logging.handlers import TimedRotatingFileHandler
from WXBizMsgCrypt import WXBizMsgCrypt
from dbhelper import dbhelper
from loadfeed import loadfeed

# hwxxTf4QLCTF
urls = ('/hello', 'hello',
        '/weixin', 'weixin'
       )
 
class hello(object):
    def GET(self):
        db = dbhelper()
        db.add(web.ctx.ip, web.ctx.homedomain+web.ctx.fullpath, web.data());
        return 'hello world'

class weixin:
    def __init__(self):        
        logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='log/app.log',
                filemode='w')
        #self.log_TimedRotatingFileHandler()

        self.request = web.input()
        self.requestdata = web.data()

        self.db = dbhelper()
        self.db.add(web.ctx.ip, web.ctx.homedomain+web.ctx.fullpath, web.data());
        
        #logging.info(self.requestdata)
        self.TOKEN = 'doumitest';
        self.EncodingAESKey = "2JNBFX4wjJmHY5EHfvWG0ZzYzMUQJrHu4T3u5sO8ZHz" 
        self.APPID = "wx3386db73536a091d"
        self.encrypt_type = ''
        try:
            if self.request.nonce is not None:
                self.nonce = self.request.nonce
            if self.request.timestamp is not None:
                self.timestamp = self.request.timestamp
            if hasattr(self.request, 'encrypt_type'):
                self.encrypt_type = self.request.encrypt_type
            if hasattr(self.request, 'msg_signature'):
                self.msg_signature = self.request.msg_signature
        except Exception, e:
            logging.error(e, exc_info=True)
        return
    
    def log_TimedRotatingFileHandler(self):
        # 定义日志输出格式
        fmt_str = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
        # 初始化
        logging.basicConfig()

        # 创建TimedRotatingFileHandler处理对象
        # 间隔5(S)创建新的名称为myLog%Y%m%d_%H%M%S.log的文件，并一直占用myLog文件。
        fileshandle = logging.handlers.TimedRotatingFileHandler('log/log', when='D', interval=1, backupCount=0)
        # 设置日志文件后缀，以当前时间作为日志文件后缀名。
        fileshandle.suffix = "%Y%m%d.log"
        # 设置日志输出级别和格式
        fileshandle.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt_str)
        fileshandle.setFormatter(formatter)
        # 添加到日志处理对象集合
        logging.getLogger('').addHandler(fileshandle)

    def ENCRYPT(self, to_xml):
        encryp_test = WXBizMsgCrypt(self.TOKEN,self.EncodingAESKey,self.APPID)
        ret,encrypt_xml = encryp_test.EncryptMsg(to_xml, self.nonce)   
        return encrypt_xml 

    def DECRYPT(self, from_xml):       
        decrypt_test = WXBizMsgCrypt(self.TOKEN,self.EncodingAESKey,self.APPID)
        ret ,decrypt_xml = decrypt_test.DecryptMsg(from_xml, self.msg_signature, self.timestamp, self.nonce)
        return decrypt_xml

    def GET(self):
		echostr = self.request.echostr
		if self.verification() and echostr is not None:
			return echostr
		return 'access verification fail'

    def POST(self):
        if True or self.verification():
            data = self.requestdata
            if self.encrypt_type == 'aes':
                data = self.DECRYPT(data)
            if data == None:
                logging.error('data decrypt fail')
                return 'data decrypt fail'
            msg = self.parse_msg(data)

            if self.user_subscribe_event(msg):
                return self.help_info(msg)
            if self.user_click_event(msg):
                return self.handle_click(msg)
            elif self.is_text_msg(msg):
                content = msg['Content']
                if content == u'?' or content == u'？':
                    return self.response_news_msg(msg)
                else:
                    return self.response_news_msg(msg)
        return 'message processing fail'
	
    def parse_msg(self, rawmsgstr):
        root = ET.fromstring(rawmsgstr)
        msg = {}
        for child in root:
            msg[child.tag] = child.text
        return msg

    # 验证
    def verification(self):
        try:
            signature = self.request.signature
            timestamp = self.request.timestamp
            nonce = self.request.nonce

            token = self.TOKEN
            tmplist = [token, timestamp, nonce]
            tmplist.sort()
            tmpstr = ''.join(tmplist)
            hashstr = hashlib.sha1(tmpstr).hexdigest()
            if hashstr == signature:
                return True 
            return False
        except Exception, e:
            logging.error(e, exc_info=True)
            return False
    
    def is_text_msg(self, msg):
        return msg['MsgType'] == 'text'

    def user_subscribe_event(self, msg):
        return msg['MsgType'] == 'event' and msg['Event'] == 'subscribe'

    def user_click_event(self, msg):
        return msg['MsgType'] == 'event' and msg['Event'] == 'CLICK'

    HELP_INFO = \
	u"""
	欢迎关注^_^
	直接关键字，即可查询
	"""

    def help_info(self, msg):
        return self.response_text_msg(msg, self.HELP_INFO)
    
    def handle_click(self, msg):
        eventKey = msg["EventKey"]
        if eventKey == 'V1001_HELLO_WORLD':
            return self.response_text_msg(msg, eventKey)

    TEXT_MSG_TPL = \
	u"""
	<xml>
	<ToUserName><![CDATA[%s]]></ToUserName>
	<FromUserName><![CDATA[%s]]></FromUserName>
	<CreateTime>%s</CreateTime>
	<MsgType><![CDATA[text]]></MsgType>
	<Content><![CDATA[%s]]></Content>
	</xml>
	"""

    def response_text_msg(self, msg, content):
        msg = self.TEXT_MSG_TPL % (msg['FromUserName'], msg['ToUserName'], str(int(time.time())), 
        content)
        if self.encrypt_type == 'aes':
            msg = self.ENCRYPT(msg.encode("utf-8"))
        logging.info(msg)
        return msg
    
    def response_xhj_msg(self, content):
        if self.encrypt_type == 'aes':
            content = self.ENCRYPT(content.encode("utf-8"))
        logging.info(content)
        return content

    NEWS_MSG_TAIL = \
	u"""
	</Articles>
	<FuncFlag>1</FuncFlag>
	</xml>
	"""

    NEWS_MSG_HEADER_TPL = \
    u"""
    <xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType><![CDATA[news]]></MsgType>
    <ArticleCount>%d</ArticleCount>
    <Articles>
    """

    NEWS_MSG_TAIL = \
    u"""
    </Articles>
    </xml>
    """

	#消息回复，采用news图文消息格式
    def response_news_msg(self, recvmsg):
        _feed = loadfeed()
        books = _feed.getfeed("http://www.uwebs.tk/feed.xml")
        msgHeader = self.NEWS_MSG_HEADER_TPL % (recvmsg['FromUserName'], recvmsg['ToUserName'], 
            str(int(time.time())), len(books))
        msg = ''
        msg += msgHeader
        msg += self.make_articles(books)
        msg += self.NEWS_MSG_TAIL
        logging.info(msg)
        if self.encrypt_type == 'aes':
            msg = self.ENCRYPT(msg.encode("utf-8"))
        
        return msg

    def make_articles(self, books):
        msg = ''
        if len(books) == 1:
            msg += self.make_single_item(books[0])
        else:
            for i, book in enumerate(books):
                msg += self.make_item(book, i+1)
        return msg
    
    NEWS_MSG_ITEM_TPL = \
    u"""<item>
        <Title><![CDATA[%s]]></Title>
        <Description><![CDATA[%s]]></Description>
        <PicUrl><![CDATA[%s]]></PicUrl>
        <Url><![CDATA[%s]]></Url>
    </item>"""

    #图文格式消息只有单独一条时，可以显示更多的description信息，所以单独处理
    def make_single_item(self, book):
        title = u'%s' % (book['title'])
        description = ''
        picUrl = book['images']
        url = book['link']
        item = self.NEWS_MSG_ITEM_TPL % (title, description, picUrl, url)
        return item

    def make_item(self, book, itemindex):
        title = u'%s' % (book['title'])
        description = ''
        picUrl = book['images'] if itemindex == 1 else book['images']
        url = book['link']
        item = self.NEWS_MSG_ITEM_TPL % (title, description, picUrl, url)
        return item

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
