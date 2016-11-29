#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import os,web,time
import sqlite3 as db

class dbhelper:
    def __init__(self):
         if os.path.exists("db/local.db"):
             #如果数据库存在，就直接连接
             self.conn = db.connect("db/local.db")
             self.cu = self.conn.cursor()
         else:
             #如果数据库不存在，连接，并生成表
             self.conn = db.connect("db/local.db")
             self.cu = self.conn.cursor()
             self.cu.execute("""create table accesslog(
                      id integer not null primary key autoincrement,
                      accessip text,
                      accessurl text,
                      date timestamp,
                      content text) """)
             self.conn.commit()

    def add(self, ip, url, content):
        self.cu.execute("""insert into accesslog(accessip, accessurl, date, content) values('%s', '%s', '%s', '%s')"""
        %(ip, url, time.strftime("%Y-%m-%d %H:%M:%S"), content)
        )
        self.conn.commit()
