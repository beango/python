#!/usr/bin/env python
# -*- coding: utf-8 -*-
# sockdemo.py
#
# test

import Queue,os,signal,time

QCOUNT = Queue.Queue() #初始化队列  
def exithanddle(s,e):  
    raise SystemExit('收到终止命令,退出程序')    
  
signal.signal(signal.SIGINT,exithanddle) #当按下Ctrl + C 终止进程  
     
while 1:    
    print '我的pid是',os.getpid()    
    print '现在队列中元素的个数是',QCOUNT.qsize()    
    time.sleep(1) 