#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3

class DbUtil():
	"""docstring for DbUtil"""
	# def __init__(self,):
	# 	super(DbUtil, self).__init__()

	def getall(self):
		conn = sqlite3.connect("wlstock.s3db")
		cu = conn.cursor()
		cu.execute("select * from mystock")
		cuall = cu.fetchall()
		return cuall
	def getone(self, stockno):
		conn = sqlite3.connect("wlstock.s3db")
		cu = conn.cursor()
		cu.execute("select * from mystock where stockno=?", (stockno,))
		return cu.fetchone()

	def insertone(self, stockno, stocktype):
		if self.getone(stockno) != None:
			return False
		conn = sqlite3.connect("wlstock.s3db")
		cu = conn.cursor()
		cu.execute("insert into mystock(stockno, stocktype) values(?, ?)", (stockno,stocktype,))
		conn.commit()
		self.close_all(conn, cu)
		return True

	def delstock(self, stockno):
		conn = sqlite3.connect("wlstock.s3db")
		cu = conn.cursor()
		cu.execute("delete from mystock where stockno=?", (stockno,))
		conn.commit()
		self.close_all(conn, cu)
		return True

	def close_all(self, conn, cu):
	     '''关闭数据库游标对象和数据库连接对象'''
	     try:
	         if cu is not None:
	             cu.close()
	     finally:
	         if cu is not None:
	             cu.close()
		
if __name__ == "__main__":
	d = DbUtil()
	print d.getall()	
	print d.getone('000001')