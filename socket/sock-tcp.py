#!/usr/bin/env python
# -*- coding: utf-8 -*-
# sockdemo.py
#
# 网络编程
import sys, datetime, time
import thread
import socket
import struct
#reload(sys)
#sys.setdefaultencoding("utf-8")

def sock_tcp_method_file(_arg):
	formatter = '128sI'
	FILEINFO_SIZE=struct.calcsize(formatter)
	connect, address = _arg[0], _arg[1]

	data = connect.recv(FILEINFO_SIZE)
	if not data:
		return;
	filename, filesize=struct.unpack(formatter,data)
	print "[%s][%s:%s]" % (
		datetime.datetime.now().strftime('%H:%M:%S'),
		address[0],
		address[1]
	)
	recvlen = 0
	f = open("new-"+filename.strip('\00').decode("utf-8"),"wb")
	while recvlen<filesize:
		data = connect.recv(1024)
		if not data:
			return;
		f.write(data)
		recvlen += len(data)
    
	f.close()
	connect.send('the result is complete!')
	connect.close()

def sock_tcp_method_msg(_arg):
	connect, address = _arg[0], _arg[1]

	data = connect.recv(1024)
	if not data:
		return;
	#print data
    
	connect.send('the result is complete!')
	connect.close()

def sock_tcp():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		sock.bind(("localhost", 12345))
	except socket.error, msg:
		print msg

	sock.listen(10)
	print "begin listening localhost:12345..."
	while 1:
		thread.start_new_thread(sock_tcp_method_msg,(sock.accept(),))

def sock_udp():
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		sock.bind(("localhost", 12346))
	except socket.error, msg:
		print msg
	print "begin listening localhost:12346..."
	while 1:
		data, client = sock.recvfrom(1024)
		if not data: break
		sock.sendto("have received!",client)
	sock.close()

'''
多线程　ThreadingTCPServer
'''
from SocketServer import ThreadingTCPServer, StreamRequestHandler 
import traceback

class MyStreamRequestHandlerr(StreamRequestHandler):  
    def handle(self):  
        while True:  
            try:  
                data = self.rfile.readline().strip()  
                print "receive from (%r):%r" % (self.client_address, data)  
                self.wfile.write(data.upper())  
            except:  
                #traceback.print_exc()  
                break  

def main():
	server = ThreadingTCPServer(("localhost",12345), MyStreamRequestHandlerr)
	server.serve_forever()

sock_tcp()

