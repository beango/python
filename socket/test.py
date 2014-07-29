#!/usr/bin/env python
# -*- coding: utf-8 -*-
# sockdemo.py
#
# test

import struct, threading, signal

a = ''

if not a:
	print 'a'
else:
	print 'b'

import datetime, time, os

print datetime.datetime.now().strftime('%m-%d %H:%M:%S')

def double(x): return x*x

arr = [1, 2, 3, 4, 5]
print map(double, arr)
print 2**16
print struct.calcsize('128s32sI8s')

_pack = struct.pack('128s8sI8s','abc','huad',1,'666')
print repr(_pack)
a,b,c,d = struct.unpack('128s8sI8s',_pack)
print a.strip('\00')

now = datetime.datetime.now()

isstop = False

def handler():
	print 'control C'
	isstop = True

def doStress():
	print 123222
	while not isstop:
		time.sleep(1)
		print 'doStress', datetime.datetime.now()

#signal.signal(signal.SIGINT, handler)
#signal.signal(signal.SIGTERM, handler)

t = threading.Thread(target=doStress, args=())
t.setDaemon(True)
t.start()
print 'complete', datetime.datetime.now()

