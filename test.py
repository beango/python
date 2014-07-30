#!/usr/bin/env python
# -*- coding: utf-8 -*-
# test.py
#
# 读取ＥＸＣＥＬ文件.

import  xdrlib ,sys
import xlrd, csv

reload(sys)
sys.setdefaultencoding( "utf-8" )

def outForList(content, row):
    for i in range(row):
        tmp = content[i::row]
        row_content = ''
        for j in tmp:
            row_content += str(j).ljust(15)
        print row_content

def load_xls():
	data = xlrd.open_workbook("4d7923f1-452f-461c-b837-eb31b6c7ed0e.xls")
	sheet1 = data.sheets()[0]
	nrows = sheet1.nrows
	ncols = sheet1.ncols
	rst = []

	for x in xrange(1, nrows):
		_r = ''.join([v.ljust(15) for v in sheet1.row_values(x)])
		rst.append(_r)
	print len(rst)

def load_csv():
	csvfile = file('2014-07-16-13-22-54_222_204.csv', 'rb')
	reader = csv.reader(csvfile)
	rst = []

	for line in reader:
		#_r = ''.join([_v.ljust(15) for _v in ''.join(line).split()]).decode('gbk').encode("utf-8")
		#_r = '|'.join(line).split() #).decode('gbk').encode("utf-8")
		#rst.append(_r)
		print '|'.join(''.join(line).split()).decode('gbk').encode("utf-8")
	print len(rst)

from module.timer import Timer

with Timer() as t:
	load_csv()
print "=> load_csv elasped lpush: %s s" % t.secs

'''
with Timer() as t:
	load_xls()
print "=> load_xls elasped lpush: %s s" % t.secs
'''