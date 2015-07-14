#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading, time
class TimerClass(threading.Thread):
	def __init__(self, internal, func):
		threading.Thread.__init__(self)
		self.event = threading.Event()
		self.internal = internal
		self.func = func

	def run(self):
		while not self.event.is_set():# self.count > 0 and 
			self.func() 
			
			self.event.wait(self.internal)

	def stop(self):
		self.event.set()

	def resume(self):
		self.event.clear()
		self.run()

def test1():
	print time.strftime('%Y-%m-%d %H:%M:%S')
	
if __name__ == "__main__":
	t = TimerClass(1, test1)
	t.start()
	time.sleep(1)
	t.stop()
	time.sleep(5)
	t.resume()