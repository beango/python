#-*- coding: utf-8 -*-
import cmd, time
import string, sys
import subprocess
from socket import *

class CLI(cmd.Cmd): 
	HOST='127.0.0.1'
	PORT=8000
	BUFSIZ=1024
	ADDR=(HOST, PORT)

	def __init__(self): 
		cmd.Cmd.__init__(self)

	def do_hello(self, data): 
		sub_cmd = subprocess.Popen("adb shell am broadcast -a NotifyServiceStop", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
		time.sleep(1)
		str = "adb forward tcp:8000 tcp:9000" 
		print str
		sub_cmd = subprocess.Popen(str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
		print sub_cmd.communicate()[0]
		time.sleep(1)
		sub_cmd = subprocess.Popen("adb shell am broadcast -a NotifyServiceStart", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
		time.sleep(1)
		client=socket(AF_INET, SOCK_STREAM)
		client.connect(self.ADDR)
		client.send(data.encode('utf8'))
		data=client.recv(self.BUFSIZ)
		if not data:
			return
		print(data.decode('utf8'))

cli = CLI()
cli.do_hello("1")
p = subprocess.Popen('dir', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#for line in p.stdout.readlines():
#    print line,
#retval = p.wait()
