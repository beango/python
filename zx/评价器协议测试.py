#!/usr/bin/python 
# -*- coding: utf-8 -*-  
import sys,time,random,types
import socket,os,struct
#from socket import *
import socket


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
    send_data = U"S01AB0001E"
    sock.sendto(send_data.encode('utf-8'), dest_addr)
    # 5. 关闭套接字
    sock.close()

def send25():
    # 1. 创建udp套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 2. 准备接收方的地址
    # '192.168.1.103'表示目的ip地址
    # 8080表示目的端口
    dest_addr = (add, 8001)
    # 3. 从键盘获取数据
    #D,0001,1,3,W,内儿科门诊,3002,黄宇,张*3,E
    send_data = U"{\"command\":\"welcome\",\"sno\":\"1\"}" #S94STOPE - S94E
    send_data = U"S06E"
    sock.sendto(send_data.encode('utf-8'), dest_addr)
    # 5. 关闭套接字
    sock.close()

def aprise():
    # 1. 创建udp套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 2. 准备接收方的地址
    # '192.168.1.103'表示目的ip地址
    # 8080表示目的端口
    dest_addr = ('192.168.1.33', 8001)
    # 3. 从键盘获取数据
    #D,0001,1,3,W,内儿科门诊,3002,黄宇,张*3,E
    send_data = U"{\"command\":\"apprise\",\"serialname\":\"综合业务\",\"sno\":\"1\",\"transcodeid\":\"id-0001-0001\",\"hcpurl\":\"http://www.baidu.com\"}" #S94STOPE - S94E
    #send_data = U"S02E"
    sock.sendto(send_data.encode('utf-8'), dest_addr)
    # 5. 关闭套接字
    sock.close()

def hcplw():
    # 1. 创建udp套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 2. 准备接收方的地址
    # '192.168.1.103'表示目的ip地址
    # 8080表示目的端口
    dest_addr = (add, 8001)
    # 3. 从键盘获取数据
    #D,0001,1,3,W,内儿科门诊,3002,黄宇,张*3,E
    send_data = U"{\"command\":\"hcp-lw\",\"sno\":\"1\",\"transcodeid\":\"id-0001-0001\",\"hcpurl\":\"file:///sdcard/hcp/index.html\"}"
    # send_data = U"{\"command\":\"hcp-lw\",\"sno\":\"1\",\"transcodeid\":\"id-0001-0001\",\"hcpurl\":\"http://www.baidu.com\"}" #S94STOPE - S94E
    # send_data = U"{\"command\":\"hcp-lw\",\"sno\":\"1\",\"transcodeid\":\"id-0001-0001\",\"hcpurl\":\"http://10.194.253.88:8082/main/evaluatereq/pad/score?acceptDate=2020-09-25%2009:32:39&certType=10&SBLSH=lw0074936372009250297513&proDepartId=007493637&proStatus=%E5%8A%9E%E7%BB%93&sign=459eb3ce196dc815f8996bf1baa76c2c&resultDate=2020-10-13%2015:16:15&hallCode=23144327010058265&taskType=2&areaName=%E8%8D%94%E6%B9%BE%E5%8C%BA&proDepart=%E8%8D%94%E6%B9%BE%E5%8C%BA%E5%8D%AB%E7%94%9F%E5%81%A5%E5%BA%B7%E5%B1%80&phonumber=38f081fd68ce405dc77ad68aecd00e4c&appId=006429D4E0&userCert=9b7f802475421a4436c081967da51ba043da81fae7587d7a&subMatter=1&timestamp=1602576836398&userName=%E6%9D%A8%E5%85%89%E5%86%9B&areaId=440103&pf=4&taskName=%E5%8C%BB%E5%B8%88%E6%89%A7%E4%B8%9A%E8%AF%81%E4%B9%A6%EF%BC%88%E5%8F%98%E6%9B%B4%EF%BC%89&projectId=11440103007493637K4440120012002202009250310&taskId=11440103007493637K4440120012002&deptCode=11440103007493637K&proManager=%E8%91%A3%E5%AE%81&proManagerNo=11191\"}"
    sock.sendto(send_data.encode('utf-8'), dest_addr)
    # 5. 关闭套接字
    sock.close()

def complete(): #来赢，荔湾政务中心接口，停止录音并发送评价数据（没有评价结果，只是为了上传录音）
    # 1. 创建udp套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 2. 准备接收方的地址
    # '192.168.1.103'表示目的ip地址
    # 8080表示目的端口
    dest_addr = (add, 8001)
    # 3. 从键盘获取数据
    #D,0001,1,3,W,内儿科门诊,3002,黄宇,张*3,E
    # send_data = U"{\"command\":\"hcp-lw\",\"sno\":\"1\",\"transcodeid\":\"id-0001-0001\",\"hcpurl\":\"http://www.baidu.com\"}" #S94STOPE - S94E
    send_data = U"{\"command\":\"complete\",\"extra\":\"queuenum=AAA&bizid=123&bizname=业务1\"}"
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
 
def reset():
    # 1. 创建udp套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 2. 准备接收方的地址
    # '192.168.1.103'表示目的ip地址
    # 8080表示目的端口
    dest_addr = (add, 8001)
    # 3. 从键盘获取数据
    #D,0001,1,3,W,内儿科门诊,3002,黄宇,张*3,E
    send_data = U"{\"command\":\"reset\",\"sno\":\"10000\"}" #S94STOPE - S94E
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

def test():
    # 1. 创建udp套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 2. 准备接收方的地址
    # '192.168.1.103'表示目的ip地址
    # 8080表示目的端口
    dest_addr = (add, 10000)
    # 3. 从键盘获取数据
    #D,0001,1,3,W,内儿科门诊,3002,黄宇,张*3,E
    t = str(time.mktime(time.localtime()))
    t = t[0:10]
    send_data = t + " , " + t
    send_data = str.strip(sys.argv[1])
    sock.sendto(send_data.encode('utf-8'), dest_addr)
    # 5. 关闭套接字
    sock.close()

def tcptest():
    serverName = '192.168.1.100'
    serverPort = 9901
    clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    
    clientSocket.send('{"Service":"VCall.Login", "UserID":"11191", "Window":"31"}'.encode())
    clientSocket.close()

def test33():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 2. 准备接收方的地址
    # '192.168.1.103'表示目的ip地址
    # 8080表示目的端口
    dest_addr = (add, 8001)
    # 3. 从键盘获取数据
    send_data = '{"command":"close"}'
    sock.sendto(send_data.encode('utf-8'), dest_addr)
    # 5. 关闭套接字
    sock.close()
   

add = '192.168.1.42'

if __name__ == '__main__':
    # pause()
    # reset()
    # time.sleep(3)
    # login()
    # time.sleep(3)
    # hcplw()
    # time.sleep(7)
    # welcome()
    # complete()
    # unlogin()

    # time.sleep(3)
    # login()
    # time.sleep(3)
    # pause()
    # time.sleep(3)
    test33()
    # time.sleep(10)
    # welcome()
