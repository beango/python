#!/usr/bin/python2.6  
# -*- coding: utf-8 -*-  
import sys,time,random
reload(sys)
sys.setdefaultencoding('utf8')

from socket import *

# 1. 创建udp套接字
udp_socket = socket(AF_INET, SOCK_DGRAM)

# 2. 准备接收方的地址
# '192.168.1.103'表示目的ip地址
# 8080表示目的端口
dest_addr = ('192.168.1.126', 9002)  # 注意 是元组，ip是字符串，端口是数字

# 3. 从键盘获取数据


for num in range(100,200):
	send_data = "请%d号李世民到%d号窗口" % (num,random.randint(1, 20)) 
	# 4. 发送数据到指定的电脑上的指定程序中
	udp_socket.sendto(send_data.encode('gb2312'), dest_addr);
	time.sleep(8)

# 5. 关闭套接字
udp_socket.close()
