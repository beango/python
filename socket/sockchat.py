import socket,struct,thread
import uuid
import signal

class sockchat:
	formatter = '8s8s128s'
	def __init__(self): 
		pass
	sock = None
	def connectServ(self, uname):
		sockchat.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sockchat.sock.connect(('localhost', 12345))
		self.uname = uname
		fhead=struct.pack(sockchat.formatter,'login',uname,'')
		sockchat.sock.send(fhead)
		res = sockchat.sock.recv(2048)
		#sockchat.sock.close()
		#
		#thread.join()
		return res
	
	def closeServ(self):
		data=struct.pack(sockchat.formatter,'logoff',self.uname,'')
		sockchat.sock.send(data)
		sockchat.sock.close()

	def recvChat(self):
		while 1:
			msg = sockchat.sock.recv(1024)
			print msg

	def sendChat(self, toname, msg):
		sendsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sendsock.connect(('localhost', 12345))
		data1=struct.pack(sockchat.formatter,'send',toname,msg)
		sendsock.send(data1)
		print sendsock.recv(2048)
		sendsock.close()

#chat.sendChat("user1","1231")
#chat.closeServ()