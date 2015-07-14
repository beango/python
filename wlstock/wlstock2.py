#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, re, os, time, threading
reload(sys)
sys.setdefaultencoding("utf-8")
import pyHook
import pythoncom
import getpass
import getk
from collections import OrderedDict
from Color import Color
from TimerClass import TimerClass
from LRUCache import LRUCache
from StockUtil import StockUtil
from dbutil import DbUtil

cache = LRUCache(100)
stockutil = StockUtil()
dbutil = DbUtil()

def delayrun():
	os.system("cls")
	cachekey = 'mystock_cuall'
	stocklist = cache.get(cachekey);
	if stocklist==None:
		stocklist = dbutil.getall()
		cache.set(cachekey,stocklist)

	clr = Color()
	head_format = "%-6s| %-13s| %-6s| %-6s| %-6s"
	headprintstr = head_format % (u'代码',
			u'名称', u'最新价',
			u'涨跌额',
			u'涨跌幅')
		
	clr.print_white_text(headprintstr)
	print '\n'
	
	idx = 0

	stockliststr = ""
	for stockitem in stocklist:
		stock = stockitem[1]
		stocktype = stockitem[2]
		stockliststr += ","+stocktype+stock+""
	if(stockliststr!=""):
		stocklistinfo = stockutil.getstockbatch(stockliststr[1:]) #获取stock
		for stockitem in stocklist:
			stockno = stockitem[1]
			stockinfo = stocklistinfo[stockno]
			stocktype = stockinfo["stocktype"]
			stocktypenam = ""
			if stocktype=="sz":
				stocktypenam = u"深"
			if stocktype=="sh":
				stocktypenam = u"上"
			if None == stockinfo:
				break;
			
			stockname = stockinfo['stockname']
			stockname = stockname+u"（"+stocktypenam+u"）" #股票名称  
			nowprice = float(round(float(stockinfo['curprice']),2)) # 最新价
			yesprice = float(round(float(stockinfo['yesendprice']),2)) # 前收盘价
			todaymaxprice = float(round(float(stockinfo['todaymaxprice']),2)) # 前收盘价
			todayminprice = float(round(float(stockinfo['todayminprice']),2)) # 前收盘价
					
			clr.print_white_text("%s " % (stockno))
			clr.print_white_text("|")
			clr.print_white_text("%s" % (stockname))
			clr.print_white_text("|")
			clr.print_white_text("%-8.2f" % (nowprice))
			clr.print_white_text("|")
			if nowprice>0 and nowprice-yesprice>0:
				clr.print_red_text("%-8.2f" % (nowprice-yesprice))
			elif nowprice>0 and nowprice-yesprice<0:
				clr.print_green_text("%-8.2f" % (nowprice-yesprice))
			else:
				clr.print_white_text("%-8.2s"%(""))
			clr.print_white_text("|")
			if nowprice>0 and nowprice-yesprice>0:
				clr.print_red_text("%-4s"%(str(round((nowprice-yesprice)*100/yesprice,2))+'%'))
			elif nowprice>0 and nowprice-yesprice<0:
				clr.print_green_text("%-4s"%(str(round((nowprice-yesprice)*100/yesprice,2))+'%'))
			else:
				clr.print_white_text("%-4s"%(""))
			print '\n'
			idx+=1

tmr = TimerClass(3, delayrun)
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
				res = stockutil.chkstock(sno)
				if res[0] == True :
					if dbutil.insertone(res[1], res[2]) == False:
						print u'已经存在'
						stockno = raw_input(u"input stock no: ")
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
	#t1.start()
	while True:
		time.sleep(1)
	#time.sleep(9999)
