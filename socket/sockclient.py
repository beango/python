#!/usr/bin/env python
# -*- coding: utf-8 -*-
# sockdemo.py
#
# 网络编程

import socket, struct
import os

def sock_tcp_test():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    sock.connect(('localhost', 12345)) 

    filename=u"test.py"#贵金属ftp文件型数据导入.txt
    fhead=struct.pack('128sI',filename.encode("utf-8"),os.stat(filename).st_size)
    sock.send(fhead)

    file = open(filename,'rb')
    while 1:
        d = file.read(1024)
        if not d:
            break
        sock.send(d)
    file.close()

    exist = 1
    if exist == 1:
        data = '\rexit'
        sock.send(data)  
        receivedData = sock.recv(1024)  
        print receivedData  

    sock.close()  

def sock_udp_test():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    sock.sendto('fhead', ('localhost', 12346))
    print sock.recvfrom(1024)

#sock_tcp_test()
#并发
def connToServer (sockIndex):
    #创建一个socket连接到127.0.0.1:8081，并发送内容
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(("127.0.0.1", 12345))
    conn.send("hi,I'm NO."+ str(sockIndex))
    while True:
        rev = conn.recv(1024)
        #print 'get server msg:' + str(rev)
        break

import sys
sys.path.append("..")
import thread,threading
from module.timer import Timer

with Timer() as ttime:
    threads = []
    times = 20000

    for i in range(0,times):
        t = threading.Thread(target=connToServer(i))
        threads.append(t)
    for i in range(0,times):
        threads[i].start()
    for i in range(0,times):
        threads[i].join()
print "=> load_csv elasped lpush: %s s" % ttime.secs

