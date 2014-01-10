#!/usr/bin/env python
# -*- coding: utf-8 -*-
# chatserv.py
#
# sockchat serv

import sys, os, socket, thread, time
import datetime

class httpserv:
	def __init__(self, port):
		# 服务器名字/版本号
		self.server_name = "MyServerDemo/0.1"
		self.GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error, msg:
			print 'socket create failed!'
		try:
			self.sock.bind(('localhost',port))
		except socket.error, msg:
			print 'socket bind failed!'
		try:
			self.sock.listen(1024)
			#self.sock.setblocking(0)
			print 'begin listen localhost:', port
		except socket.error, msg:
			print 'socket listen failed!'
	'''
	' ab -n 1000 -c 10 http://localhost:12345/123.html
	' Requests per second:    19.84 [#/sec]
	  50%    502
	  66%    507
	  75%    510
	  80%    514
	  90%   1000
	  95%   1006
	  98%   1015
	  99%   1019
	 100%   1500 (longest request)
	'''
	def run_single(self):
		try:
			while 1:
				try:
					conn, address = self.sock.accept()
					conn.setblocking(0)
				except socket.error, msg:
					time.sleep(0.01)
					continue

				while 1:
					try:
						data = conn.recv(2048)
					except socket.error, msg:
						time.sleep(0.01)
						continue

					if len(data)==0: break
					if not data:break
					arr_head = data.split('\r\n')
					request_url = arr_head[0].split(' ')[1].split('?')[0]
					filepath = "content" + request_url
					now = datetime.datetime.utcnow()
					expires = datetime.timedelta(seconds=60)
					
					if os.path.isfile(filepath):
						response_code = "200 OK"
						content = open(filepath, 'rb').read()
					else:
						response_code = "400 Not Found"
						content = "<h1>Page not found!</h1>"

					response = '''HTTP/1.1 %s\r\nServer: %s\r\nDate: %s\r\nExpires: %s\r\nContent-Type: %s\r\nContent-Length: %s
	Connection: keep-alive\r\n\r\n%s''' % (
						response_code,
						self.server_name, 
						now.strftime(self.GMT_FORMAT), 
						(now + expires).strftime(self.GMT_FORMAT),
						self.getAccept(request_url),
						len(content),
						content
					)
					conn.send(response)
					break
				conn.close()
		except socket.error, msg:
			print msg, '无法连接'
			sys.exit()
		finally:
			self.sock.close()

	'''
	' listen = 5
	' ab -n 1000 -c 10 http://localhost:12345/123.html
	' Requests per second:    66.51 [#/sec] (mean)
	  50%    502
	  66%    510
	  75%    996
	  80%    999
	  90%   1000
	  95%   1001
	  98%   1009
	  99%   1016
	 100%   1018 (longest request)
	'''
	def run_multi(self):
		try:
			while 1:
				conn, client = self.sock.accept()
				thread.start_new_thread(self.handlerconn,((conn,self.sock),))
		except socket.error, msg:
			print msg
			sys.exit()
		finally:
			self.sock.close()

	def handlerconn(self, _args):
		conn, sock = _args[0], _args[1]
		while 1:
			data = conn.recv(2048)
			if not data:break
			arr_head = data.split('\r\n')
			request_url = arr_head[0].split(' ')[1].split('?')[0]
			print request_url
			filepath = "content" + request_url
			now = datetime.datetime.utcnow()
			expires = datetime.timedelta(seconds=60)
			
			if os.path.isfile(filepath):
				response_code = "200 OK"
				content = open(filepath, 'rb').read()
			else:
				response_code = "400 Not Found"
				content = "<h1>Page not found!</h1>"

			response = '''HTTP/1.1 %s\r\nServer: %s\r\nDate: %s\r\nExpires: %s\r\nContent-Type: %s\r\nContent-Length: %s
Connection: keep-alive\r\n\r\n%s''' % (
				response_code,
				self.server_name, 
				now.strftime(self.GMT_FORMAT), 
				(now + expires).strftime(self.GMT_FORMAT),
				self.getAccept(request_url),
				len(content),
				content
			)
			conn.send(response)
			break
		conn.close()

	def getAccept(self, _url):
		if _url.endswith(".css"):return "text/css; charset=utf-8"
		if _url.endswith(".js"):return "application/javascript"
		if _url.endswith(".gif"):return "image/gif"
		if _url.endswith(".png"):return "image/png"
		if _url.endswith(".jpg"):return "image/jpg"
		return "text/html;charset=utf-8";

serv1 = httpserv(12345)
serv1.run_single()

#serv2 = httpserv(12346)
#serv2.run_multi()