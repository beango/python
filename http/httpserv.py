#!/usr/bin/env python
# -*- coding: utf-8 -*-
# chatserv.py
#
# sockchat serv

import os, socket
import datetime

class httpserv:
	def __init__(self):
		# 服务器名字/版本号
		self.server_name = "MyServerDemo/0.1"
		self.GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'

	def run(self):
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
				#print data
				filepath = "content" + request_url
				now = datetime.datetime.utcnow()
				expires = datetime.timedelta(seconds=60)
				
				if os.path.isfile(filepath):
					response_code = "200 OK"
					content = open(filepath, 'rb').read()
				else:
					response_code = "400 Not Found"
					content = "<h1>Page not found!</h1>"

				response = '''HTTP/1.1 %s
					Server: %s
					Date: %s
					Expires: %s
					Content-Type: %s;charset=utf-8
					Content-Length: %s
					Connection: keep-alive

					%s''' % (
					response_code,
					self.server_name, 
					now.strftime(self.GMT_FORMAT), 
					(now + expires).strftime(self.GMT_FORMAT),
					self.getAccept(request_url),
					len(content),
					content
				)
				conn.send(response)
				if request_url =="/bundles/blog-common.css":
					print response
				break
			conn.close()
		sock.close()
	def getAccept(self, _url):
		if _url.endswith(".css"):return "text/css"
		if _url.endswith(".js"):return "text/javascript"
		if _url.endswith(".gif"):return "image/gif"
		if _url.endswith(".png"):return "image/png"
		if _url.endswith(".jpg"):return "image/jpg"
		return "text/html";
serv = httpserv()
serv.run()