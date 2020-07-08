#!/usr/bin/python2.6  
# -*- coding: utf-8 -*-  
import sys,time,random,types
import socket,os,struct
#from socket import *
import socket

add = '192.168.5.138'
def test1():
    # 1. 创建udp套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 2. 准备接收方的地址
    # '192.168.1.103'表示目的ip地址
    # 8080表示目的端口
    dest_addr = (add, 8001)
    # 3. 从键盘获取数据
    #D,0001,1,3,W,内儿科门诊,3002,黄宇,张*3,E
    send_data = "S02E" #S94STOPE - S94E
    sock.sendto(send_data.encode('gb2312'), dest_addr)
    # 5. 关闭套接字
    sock.close()

def bind():
    HOST = '192.168.1.10'
    PORT = 7791

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST,PORT))
    print('...waiting for message..')
    while True:
        data,address = s.recvfrom(1024)
        print(data,address)
        s.sendto('this is the UDP server',address)
    s.close()

def test2():
    # 1. 创建udp套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 2. 准备接收方的地址
    # '192.168.1.103'表示目的ip地址
    # 8080表示目的端口
    dest_addr = (add, 8001)
    # 3. 从键盘获取数据
    #D,0001,1,3,W,内儿科门诊,3002,黄宇,张*3,E
    send_data = U"{\"command\":\"apprise\",\"serialname\":\"换证业务\"}" #S94STOPE - S94E
    sock.sendto(send_data.encode('utf-8'), dest_addr)
    # 5. 关闭套接字
    sock.close()

def login():
    # 1. 创建udp套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 2. 准备接收方的地址
    # '192.168.1.103'表示目的ip地址
    # 8080表示目的端口
    dest_addr = (add, 8001)
    # 3. 从键盘获取数据
    #D,0001,1,3,W,内儿科门诊,3002,黄宇,张*3,E
    send_data = U"{\"command\":\"login\",\"sno\":\"1\"}" #S94STOPE - S94E
    sock.sendto(send_data.encode('utf-8'), dest_addr)
    # 5. 关闭套接字
    sock.close()

def unlogin():
    # 1. 创建udp套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 2. 准备接收方的地址
    # '192.168.1.103'表示目的ip地址
    # 8080表示目的端口
    dest_addr = (add, 8001)
    # 3. 从键盘获取数据
    #D,0001,1,3,W,内儿科门诊,3002,黄宇,张*3,E
    send_data = U"{\"command\":\"unlogin\",\"sno\":\"1\"}" #S94STOPE - S94E
    sock.sendto(send_data.encode('utf-8'), dest_addr)
    # 5. 关闭套接字
    sock.close()

    
    
def welcome():
    # 1. 创建udp套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 2. 准备接收方的地址
    # '192.168.1.103'表示目的ip地址
    # 8080表示目的端口
    dest_addr = (add, 8001)
    # 3. 从键盘获取数据
    #D,0001,1,3,W,内儿科门诊,3002,黄宇,张*3,E
    send_data = U"{\"command\":\"welcome\",\"sno\":\"1\"}" #S94STOPE - S94E
    sock.sendto(send_data.encode('utf-8'), dest_addr)
    # 5. 关闭套接字
    sock.close()

def aprise():
    # 1. 创建udp套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 2. 准备接收方的地址
    # '192.168.1.103'表示目的ip地址
    # 8080表示目的端口
    dest_addr = (add, 8001)
    # 3. 从键盘获取数据
    #D,0001,1,3,W,内儿科门诊,3002,黄宇,张*3,E
    send_data = U"{\"command\":\"apprise\",\"sno\":\"1\"}" #S94STOPE - S94E
    sock.sendto(send_data.encode('utf-8'), dest_addr)
    # 5. 关闭套接字
    sock.close()
    
def pause():
    # 1. 创建udp套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 2. 准备接收方的地址
    # '192.168.1.103'表示目的ip地址
    # 8080表示目的端口
    dest_addr = (add, 8001)
    # 3. 从键盘获取数据
    #D,0001,1,3,W,内儿科门诊,3002,黄宇,张*3,E
    send_data = U"{\"command\":\"pause\",\"sno\":\"10000\"}" #S94STOPE - S94E
    sock.sendto(send_data.encode('utf-8'), dest_addr)
    # 5. 关闭套接字
    sock.close()
    
def sign():
    # 1. 创建udp套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 2. 准备接收方的地址
    # '192.168.1.103'表示目的ip地址
    # 8080表示目的端口
    dest_addr = (add, 8001)
    # 3. 从键盘获取数据
    #D,0001,1,3,W,内儿科门诊,3002,黄宇,张*3,E
    send_data = U"S50E"
    sock.sendto(send_data.encode('utf-8'), dest_addr)
    # 5. 关闭套接字
    sock.close()


unlogin()
time.sleep(3)
login()
# time.sleep(3)
# pause()
# time.sleep(3)
# aprise()
# time.sleep(10)
# welcome()