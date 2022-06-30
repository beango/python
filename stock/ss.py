#!/usr/bin/env python
# -*- coding:utf-8 -*-

from colorama import init, Fore, Back, Style
from prettytable import PrettyTable 
import urllib.request
import time

#print('current_time:')
print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
print()
 
#debug=True
debug=False
x = PrettyTable(['名字', '代码', '时间', '当前价格', '涨跌', '涨跌%', '成交量(手)', '成交额(万)', '总市值(亿)'])
x.align = 'l'
x.align['涨跌%'] = 'r'
x.align['涨跌'] = 'r'

init(autoreset=False)
class Colored(object):
    #  前景色:红色  背景色:默认
    def red(self, s):
        return Fore.RED + s + Fore.RESET
    #  前景色:绿色  背景色:默认
    def green(self, s):
        return Fore.GREEN + s + Fore.RESET
    def yellow(self, s):
        return Fore.YELLOW + s + Fore.RESET
    def white(self,s):
        return Fore.WHITE + s + Fore.RESET
    def blue(self,s):
        return Fore.BLUE + s + Fore.RESET

class Utility:
    def ToGB(str):
        if(debug): print(str)
        return str.decode('gb2312')
 
class StockInfo:
 
    def GetStockStrByNum(num):
        f= urllib.request.urlopen('http://qt.gtimg.cn/q=s_'+ str(num))
        if(debug): print(f.geturl())
        if(debug): print(f.info())
        return f.readline()
        f.close()
 
    def ParseResultStr(resultstr):
        if(debug): print(resultstr)
        slist=resultstr[14:-3]
        if(debug): print(slist)
        slist=slist.split('~')
 
        if(debug) : print(slist)

        color = Colored()#创建Colored对象

        zhangdie = float(slist[4])

        if (zhangdie < 0):
            slist[1] = color.green(slist[1])
            slist[2] = color.green(slist[2])
            slist[3] = color.green(slist[3])
            slist[4] = color.green(slist[4])
            slist[5] = color.green(slist[5] + '%')
            slist[6] = color.green(slist[6])
            slist[7] = color.green(slist[7])
            slist[9] = color.green(slist[9])
        elif (zhangdie > 0):
            slist[1] = color.red(slist[1])
            slist[2] = color.red(slist[2])
            slist[3] = color.red(slist[3])
            slist[4] = color.red(slist[4])
            slist[5] = color.red(slist[5] + '%')
            slist[6] = color.red(slist[6])
            slist[7] = color.red(slist[7])
            slist[9] = color.red(slist[9])
 
        x.add_row([slist[1], slist[2], '', slist[3], slist[4], slist[5], slist[6], slist[7], slist[9]])

    def GetStockInfo(num):
        str=StockInfo.GetStockStrByNum(num)
        strGB=Utility.ToGB(str)
        StockInfo.ParseResultStr(strGB)
 
 
if __name__ == '__main__':
    stocks = [
        'sh000001',#上证指数 
	#	'sh600776',#东方通信 
	#	'sh603000',#人民网 
		'sh600000',#浦发银行 
		'sh600085',#同仁堂 
		'sh601009',#南京银行
		'sz002186',#全聚德
		'sz002425' #凯撒文化
    ]
    for stock in stocks:
        StockInfo.GetStockInfo(stock)

    print(x)