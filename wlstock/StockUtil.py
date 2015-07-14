#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, re, os, time, threading
import urllib2
reload(sys)
sys.setdefaultencoding("utf-8")

class StockUtil():
	"""docstring for StockUtil"""
	def __init__(self):
		pass

	def getstock(self, stockno, stocktype):
		try:
			pattern = re.compile(r'"(.*)"')
			sinfo = urllib2.urlopen('http://hq.sinajs.cn/list='+stocktype+stockno).read()
			if stockno == '000009':
				print sinfo
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
			print e

	def getstockbatch(self, stocknos):
		r = []
		try:
			pattern = re.compile(r'var hq_str_([a-z]*)([0-9]*)="(.*)"')
			sinfo = urllib2.urlopen('http://hq.sinajs.cn/list='+stocknos).read()
			
			for	line in sinfo.split(';'):
				if line == "":
					break
				match = pattern.split(line)
				#3 中国中车,21.99,22.45,20.52,21.99,20.50,20.52,20.53,927998443,19728191869,117680,
				#20.52,33100,20.51,2829080,20.50,70700,20.49,225400,20.48,25100,20.53,327893,20.54,
				#445788,20.55,273782,20.56,154270,20.57,2015-06-18,15:04:01,00
				if len(match)>1:
					sinfo = match[3]
					if sinfo==None or sinfo=='' or len(sinfo)==0:
						break
					ssplit = sinfo.split(',')
					# 涨跌额
					nowprice = round(float(ssplit[3]),2) # 最新价
					yesprice = round(float(ssplit[2]),2) # 前收盘价
					todaymaxprice = round(float(ssplit[4]),2) # 前收盘价
					todayminprice = round(float(ssplit[5]),2) # 前收盘价
					zde = nowprice-yesprice
					if nowprice==0:
						zde = None
					zdf2 = round((nowprice-yesprice)*100/yesprice,2)
					if nowprice==0:
						zdf2 = None
					r.append({
									'stockno': match[2],
									'stockname': ssplit[0].decode("gbk"), #股票名字
									'nowprice': nowprice, #当前价格
									'yesendprice': yesprice, #昨日收盘价
									'stocktype': match[1], #sh,sz
									'todaymaxprice': todaymaxprice, #最高价
									'todayminprice': todayminprice,
									'zde':round(zde,2),
									'zdf':round(zdf2,2)}) #最低价
		except Exception, e:
			print e
		return r
		

	def getstocktyp(self, stockno):
		if len(stockno)<3:
			return None;
		fist3 = stockno[0:3]
		if fist3=='600' or fist3=='601' or fist3=='900' or fist3=='730' or fist3=='700' or fist3=='580':
			return 'sh'
		if fist3=='000' or fist3=='002' or fist3=='200' or fist3=='300' or fist3=='080' or fist3=='031':
			return 'sz'
		return None;

	def chkstock(self, stockno):
		# existsstock = getone(stockno)
		# if existsstock != None:
		# 	print u'该股票代码已经存在'
		# 	return False
		stocktyp = self.getstocktyp(stockno)
		if stocktyp != None:
			stockinfo = self.getstock(stockno,stocktyp) #获取stock
			if stockinfo == None:
				print u'股票代码不存在！'
				return (False,);
			return (True, stockno, stocktyp)
		else:
			print u'添加失败'
			return  (False,);

if __name__ == "__main__":
	s = StockUtil()
	#print s.getstock("000001", 'sh')	
	stocklistinfo = s.getstockbatch("sh600000,sh000001,sh601179")
	print stocklistinfo
	stocklistinfo.sort(lambda x,y : cmp(x['stockno'], y['stockno']))
	print stocklistinfo