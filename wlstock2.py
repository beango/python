#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, re, threading, os, time
import urllib2, sqlite3
reload(sys)
sys.setdefaultencoding("utf-8")
import ctypes
import pyHook
import pythoncom
import getpass
import getk
from collections import OrderedDict

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12
 
# 字体颜色定义 ,关键在于颜色编码，由2位十六进制组成，分别取0~f，前一位指的是背景色，后一位指的是字体色
#由于该函数的限制，应该是只有这16种，可以前景色与背景色组合。也可以几种颜色通过或运算组合，组合后还是在这16种颜色中
 
# Windows CMD命令行 字体颜色定义 text colors
FOREGROUND_BLACK = 0x00 # black.
FOREGROUND_DARKBLUE = 0x01 # dark blue.
FOREGROUND_DARKGREEN = 0x02 # dark green.
FOREGROUND_DARKSKYBLUE = 0x03 # dark skyblue.
FOREGROUND_DARKRED = 0x04 # dark red.
FOREGROUND_DARKPINK = 0x05 # dark pink.
FOREGROUND_DARKYELLOW = 0x06 # dark yellow.
FOREGROUND_DARKWHITE = 0x07 # dark white.
FOREGROUND_DARKGRAY = 0x08 # dark gray.
FOREGROUND_BLUE = 0x09 # blue.
FOREGROUND_GREEN = 0x0a # green.
FOREGROUND_SKYBLUE = 0x0b # skyblue.
FOREGROUND_RED = 0x0c # red.
FOREGROUND_PINK = 0x0d # pink.
FOREGROUND_YELLOW = 0x0e # yellow.
FOREGROUND_WHITE = 0x0f # white.
 
 
# Windows CMD命令行 背景颜色定义 background colors
BACKGROUND_BLUE = 0x10 # dark blue.
BACKGROUND_GREEN = 0x20 # dark green.
BACKGROUND_DARKSKYBLUE = 0x30 # dark skyblue.
BACKGROUND_DARKRED = 0x40 # dark red.
BACKGROUND_DARKPINK = 0x50 # dark pink.
BACKGROUND_DARKYELLOW = 0x60 # dark yellow.
BACKGROUND_DARKWHITE = 0x70 # dark white.
BACKGROUND_DARKGRAY = 0x80 # dark gray.
BACKGROUND_BLUE = 0x90 # blue.
BACKGROUND_GREEN = 0xa0 # green.
BACKGROUND_SKYBLUE = 0xb0 # skyblue.
BACKGROUND_RED = 0xc0 # red.
BACKGROUND_PINK = 0xd0 # pink.
BACKGROUND_YELLOW = 0xe0 # yellow.
BACKGROUND_WHITE = 0xf0 # white.

class Color:
    ''' See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winprog/winprog/windows_api_reference.asp
    for information on Windows APIs. - www.sharejs.com'''
    std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
     
    def set_cmd_color(self, color, handle=std_out_handle):
        """(color) -> bit
        Example: set_cmd_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE | FOREGROUND_INTENSITY)
        """
        bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
        return bool
     
    def reset_color(self):
        self.set_cmd_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)
     
    def print_red_text(self, print_text):
        self.set_cmd_color(FOREGROUND_RED)
        print print_text,
        self.reset_color()
         
    def print_green_text(self, print_text):
        self.set_cmd_color(FOREGROUND_GREEN)
        print print_text,
        self.reset_color()
     
    def print_blue_text(self, print_text):
        self.set_cmd_color(FOREGROUND_BLUE)
        print print_text,
        self.reset_color()

    def print_white_text(self, print_text):
        self.set_cmd_color(FOREGROUND_WHITE)
        print print_text,
        self.reset_color()
           
    def print_red_text_with_blue_bg(self, print_text):
        self.set_cmd_color(FOREGROUND_RED | FOREGROUND_INTENSITY| BACKGROUND_BLUE)
        print print_text,
        self.reset_color()  

class TimerClass(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.event = threading.Event()
		#self.count = 10

	def run(self):
		while not self.event.is_set():# self.count > 0 and 
			delayrun() 
			self.event.wait(3.0)

	def stop(self):
		print 'timerclass.stop'
		self.event.set()

	def resume(self):
		print 'timerclass.start'
		self.event.clear()
		self.run()

	def join(self):
		#print 'timerclass.join'
		self.event.wait()

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.tm = 0
        self.cache = {}
        self.lru = {}

    def get(self, key):
        if key in self.cache:
            self.lru[key] = self.tm
            self.tm += 1
            return self.cache[key]
        return None

    def set(self, key, value):
        if len(self.cache) >= self.capacity:
            # find the LRU entry
            old_key = min(self.lru.keys(), key=lambda k:self.lru[k])
            self.cache.pop(old_key)
            self.lru.pop(old_key)

        self.cache[key] = value
        self.lru[key] = self.tm
        self.tm += 1
cache = LRUCache(100)
def getmystock():
	cachekey = 'mystock_cuall'
	cuall = cache.get(cachekey);
	if cuall==None:
		conn = sqlite3.connect("wlstock.s3db")
		cu = conn.cursor()
		cu.execute("select * from mystock")
		cuall = cu.fetchall()
		cache.set(cachekey,cuall)
	return cuall
def getone(stockno):
	conn = sqlite3.connect("wlstock.s3db")
	cu = conn.cursor()
	cu.execute("select * from mystock where stockno=?", (stockno,))
	return cu.fetchone()

def insertone(stockno, stocktype):
	conn = sqlite3.connect("wlstock.s3db")
	cu = conn.cursor()
	cu.execute("insert into mystock(stockno, stocktype) values(?, ?)", (stockno,stocktype,))
	conn.commit()
	close_all(conn, cu)

def close_all(conn, cu):
     '''关闭数据库游标对象和数据库连接对象'''
     try:
         if cu is not None:
             cu.close()
     finally:
         if cu is not None:
             cu.close()

def getstock(stockno, stocktype):
	try:
		pattern = re.compile(r'"(.*)"')
		sinfo = urllib2.urlopen('http://hq.sinajs.cn/list='+stocktype+stockno).read()
		match = pattern.split(sinfo)
		#3 中国中车,21.99,22.45,20.52,21.99,20.50,20.52,20.53,927998443,19728191869,117680,
		#20.52,33100,20.51,2829080,20.50,70700,20.49,225400,20.48,25100,20.53,327893,20.54,
		#445788,20.55,273782,20.56,154270,20.57,2015-06-18,15:04:01,00
		sinfo = match[1]
		if sinfo==None or sinfo=='' or len(sinfo)==0:
			return None
		ssplit = sinfo.split(',')
		return (ssplit[0].decode("gbk"), ssplit[3], ssplit[2])
	except Exception, e:
		print 'e'

def delayrun():
	os.system("cls")
	clr = Color()
	head_format = "%-8s   |   %-4s   |   %-5s   |   %-5s   |   %-4s"
	headprintstr = head_format % (u'股票代码',
			u'股票名称', u'最新价',
			u'涨跌额',
			u'涨跌幅')
		
	clr.print_white_text(headprintstr)
	print '\n'
	stocklist = getmystock()
	idx = 0

	for stockitem in stocklist:
		stock = stockitem[1]
		stocktype = stockitem[2]
		stocktypenam = ""
		if stocktype=="sz":
			stocktypenam = u"深"
		if stocktype=="sh":
			stocktypenam = u"上"
		stockinfo = getstock(stock,stocktype) #获取stock
		if None == stockinfo:
			break;
		stockno = stock+u"（"+stocktypenam+u"）" #股票名称  

		stocknam = stockinfo[0] # 代码
		nowprice = float(round(float(stockinfo[1]),2)) # 最新价
		yesprice = float(round(float(stockinfo[2]),2)) # 前收盘价
		
		header_format = "%-8s  |  %-4s  |  %-8.2f  |  %-8.2f  |  %-4s"
		
		printstr = header_format % (stockno,
			stocknam.encode("utf8"), nowprice,
			nowprice-yesprice,
			str(round((nowprice-yesprice)*100/yesprice,2))+'%')
		
		#clr.print_green_text(printstr)
		clr.print_white_text("%-8s"%(stockno))
		clr.print_white_text("  |  ")
		clr.print_white_text("%-4s"%(stocknam))
		clr.print_white_text("  |  ")
		clr.print_white_text("%-8.2f"%(nowprice))
		clr.print_white_text("  |  ")
		if nowprice>0 and nowprice-yesprice>0:
			clr.print_red_text("%-8.2f"%(nowprice-yesprice))
		elif nowprice>0 and nowprice-yesprice<0:
			clr.print_green_text("%-8.2f"%(nowprice-yesprice))
		else:
			clr.print_white_text("%-8.2s"%(""))
		clr.print_white_text("  |  ")
		if nowprice>0 and nowprice-yesprice>0:
			clr.print_red_text("%-4s"%(str(round((nowprice-yesprice)*100/yesprice,2))+'%'))
		elif nowprice>0 and nowprice-yesprice<0:
			clr.print_green_text("%-4s"%(str(round((nowprice-yesprice)*100/yesprice,2))+'%'))
		else:
			clr.print_white_text("%-4s"%(""))
		print '\n'
		idx+=1

def getstocktyp(stockno):
	if len(stockno)<3:
		return None;
	fist3 = stockno[0:3]
	if fist3=='600' or fist3=='601' or fist3=='900' or fist3=='730' or fist3=='700' or fist3=='580':
		return 'sh'
	if fist3=='000' or fist3=='002' or fist3=='200' or fist3=='300' or fist3=='080' or fist3=='031':
		return 'sz'
	return None;

def insertstock(sno):
	existsstock = getone(sno)
	if existsstock != None:
		print u'该股票代码已经存在'
		return False
	stocktyp = getstocktyp(sno)
	if stocktyp != None:
		stockinfo = getstock(sno,stocktyp) #获取stock
		if stockinfo == None:
			print u'股票代码不存在！'
			return False;
		insertone(sno,stocktyp)
	else:
		print u'添加失败'
		return  False
	return True

tmr = TimerClass()
def listenKey():
    while True:
    	print 'Press a key'
    	inkey = getk._Getch()
    	for i in xrange(sys.maxint):
	 	k=inkey()
	 	if k <> '': break
    	print 'you pressed ',k
    	if k == 'i':
			tmr.stop()
			os.system("cls")
			stockno = raw_input(u"input stock no: ")
			while True:
				sno = stockno
				res = insertstock(sno)
				if res == True :
					tmr.resume()
					return
				stockno = raw_input(u"input stock no: ")
    	elif k == 'q':
			print 'q'
			os.system("exit")
		 	return

if __name__ == "__main__":
	tmr.start()
	t1 = threading.Thread(target=listenKey)
	t1.setDaemon(True)
	t1.start()
	while True:
		time.sleep(1)
	#time.sleep(9999)
