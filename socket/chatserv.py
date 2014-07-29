#!/usr/bin/env python
# -*- coding: utf-8 -*-
# chatserv.py
#
# sockchat serv

import socket, thread
import uuid
import struct

class sockserver:
	clientlist = []
	formatter = '8s8s128s'

	def run(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind(('localhost',12345))
		sock.listen(5)
		while 1:
			conn, client = sock.accept()
			thread.start_new_thread(self.handlerconn,((conn,sock),))

	def handlerconn(self, _args):
		conn, sock = _args[0], _args[1]
		while 1:
			data = conn.recv(2048)
			if not data: break;

			action, uname, data = struct.unpack(sockserver.formatter,data)
			action = action.strip('\00')
			uname = uname.strip('\00')
			data = data.strip('\00')
			if "login"==action:
				uid = uuid.uuid4()
				sockserver.clientlist.append({'uid':uid, 'name':uname, 'conn':conn})
				print uname+"joind!"
				conn.send(str(uid))

			if "logoff"==action:
				for c in sockserver.clientlist:
					if c["name"] == uname: del sockserver.clientlist[sockserver.clientlist.index(c)]
				print uname, "logoff succ!"
				conn.send("logoff succ")
				break

			if "send"==action:
				to = None
				for c in sockserver.clientlist:
					if c["name"] == uname: to = c["conn"]
				if not to : 
					print "not found user"
					break
				to.send(uname+": "+data)
				conn.send("send succ")
		conn.close()

	def run2(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind(('localhost',12345))
		sock.listen(5)
		while 1:
			conn, client = sock.accept()
			data = conn.recv(2048)
			print client, data
			conn.close()
		sock.close()

serv = sockserver()
serv.run()