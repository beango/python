#!/usr/bin/env python
# -*- coding: utf-8 -*-
# test.py
#
# 读取ＥＸＣＥＬ文件.

import  xdrlib ,sys
import xlrd, csv

reload(sys)
sys.setdefaultencoding( "utf-8" )

def load_xls():
	data = xlrd.open_workbook("4d7923f1-452f-461c-b837-eb31b6c7ed0e.xls")
	sheet1 = data.sheets()[0]
	nrows = sheet1.nrows
	ncols = sheet1.ncols

	for x in xrange(1, nrows):
		print ''.join([v.ljust(15) for v in sheet1.row_values(x)])

def load_csv():
	csvfile = file('2014-07-16-13-22-54_222_204.csv', 'rb')
	reader = csv.reader(csvfile)
	for line in reader:
		_r = ''.join([_v.ljust(15) for _v in ''.join(line).split()]).decode('gbk').encode("utf-8")
	csvfile.close()

import sys
sys.path.append("module")

from timer import Timer

with Timer() as t:
	#load_xls()
	load_csv()
print "=> elasped lpush: %s s" % t.secs