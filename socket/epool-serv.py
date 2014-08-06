#! /usr/bin/env python  
#coding=utf-8  

import socket,select

class epollserv():
	def __init__(self):
		pass

	def run(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind(('',12345))
		sock.listen(1024)

		p = select.epool()
		p.register(sock)
		while 1:
			events = p.pool()
			pass


if __name__ == "__main__":
	print vars(select)
	sockserv = epollserv()
	sockserv.run()