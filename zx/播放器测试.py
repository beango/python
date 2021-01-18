#!/usr/bin/python
# -*- coding: utf-8 -*-  
import sys,time,random,types,socket

#from socket import *


# 1. 创建udp套接字
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. 准备接收方的地址
# '192.168.1.103'表示目的ip地址
# 8080表示目的端口
dest_addr = ('192.168.1.171', 9002)  # 注意 是元组，ip是字符串，端口是数字

# 3. 从键盘获取数据

#D,0001,1,3,W,内儿科门诊,3002,黄宇,张*3,E
send_data = U"D,1,1,22,W,内儿科门诊,0087,黄宇,张*3,E"
send_data = U'{"command":"play","playstyle":"1","speed":"40","volumn":"100","content":"请001号欧阳长林到内科门诊就诊"}'
#send_data = U"D,0001,1,9,S,内儿科门诊,3002,黄宇,张*3,E"
udp_socket.sendto(send_data.encode('gb2312'), dest_addr)

no = 0
for num in range(100,10000):
	no = no+1
	send_data = U"D,1021,%d,S%04d,W,内儿科门诊,3002,黄宇,郑林娟,E" % (random.randint(1, 20), no)
	udp_socket.sendto(send_data.encode('gb2312'), dest_addr)

	send_data = '{"command":"play","playstyle":"1","speed":"30","volumn":"100","content":"请001号欧阳长林到内科门诊就诊"}'# % (num) #,random.randint(1, 20)
	#send_data = '{"command":"play","playstyle":"1","speed":"40","volumn":"100","content":"发送数据到指定的电脑上的指定程序中"}'
	send_data = U'{"command":"play","playstyle":"1,2",speed:"45","volumn":"100","content":"请A%d号到K%d号窗口"}' % (num, random.randint(1, 20))
	#send_data = U"D,0001,%d,%d,W,内儿科门诊,3002,黄宇,张*3,E"%(random.randint(1, 10), num)
	#send_data = U"D,1,1111,%d,W,内儿科门诊,3002,黄宇,张*3,E"%num
	print(send_data)
	udp_socket.sendto(send_data.encode('gb2312'), dest_addr)

	time.sleep(5)

# 5. 关闭套接字
udp_socket.close()
