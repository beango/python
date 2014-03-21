#!/usr/bin/env python
# -*- coding: utf-8 -*-
# chatserv.py
#
# sockchat serv

import socket
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
				print data

				response_code = "200 OK"
				now = datetime.datetime.utcnow()
				expires = datetime.timedelta(seconds=60)
				content = "<h1>hello my http serv!</h1>"
				response = '''HTTP/1.1 %s
					Server: %s
					Date: %s
					Expires: %s
					Content-Type: text/html;charset=utf8
					Content-Length: %s
					Connection: keep-alive

					%s''' % (
					response_code,
					self.server_name, 
					now.strftime(self.GMT_FORMAT), 
					(now + expires).strftime(self.GMT_FORMAT),
					len(content),
					content
				)
				conn.send(response)
				conn.close()
		sock.close()

serv = httpserv()
serv.run()