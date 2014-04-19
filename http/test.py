#coding=gbk  

import time
import sys
import os


print  'hello -1'
f = os.fork()
print os.getpid()

if f == 0 : 
	print "\nEntering in child process" 
	sys.exit()