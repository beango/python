#!/usr/bin/env python
# -*- coding: utf-8 -*-
# chatserv.py
#
# sockchat serv

import sys, os, socket, thread
import datetime

class httpserv:
	def __init__(self):
		# 服务器名字/版本号
		self.server_name = "MyServerDemo/0.1"
		self.GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'

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
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.bind(('localhost',12345))
			sock.listen(5)

			while 1:
				conn, address = sock.accept()
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
		except socket.error, msg:
			print msg
			sys.exit()
		finally:
			sock.close()

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
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.bind(('localhost',12345))
			self.sock.listen(10)

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

serv = httpserv()
serv.run_multi()