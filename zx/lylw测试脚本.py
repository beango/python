#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：tcpclient.py
 
import socket
import time
MaxBytes=1024*1024
host ='192.168.1.199'
port = 9901
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.settimeout(7)
client.connect((host,port))
sendBytes = client.send('HAOCHAPING?jsonpcallback=jQuery111105298489809635909_1602576785453&TYPE=http%3A%2F%2F10.194.253.88%3A8082%2Fmain%2Fevaluatereq%2Fpad%2Fscore%3FacceptDate%3D2020-09-25%252009%3A32%3A39%26certType%3D10%26SBLSH%3Dlw0074936372009250297513%26proDepartId%3D007493637%26proStatus%3D%25E5%258A%259E%25E7%25BB%2593%26sign%3D459eb3ce196dc815f8996bf1baa76c2c%26resultDate%3D2020-10-13%252015%3A16%3A15%26hallCode%3D23144327010058265%26taskType%3D2%26areaName%3D%25E8%258D%2594%25E6%25B9%25BE%25E5%258C%25BA%26proDepart%3D%25E8%258D%2594%25E6%25B9%25BE%25E5%258C%25BA%25E5%258D%25AB%25E7%2594%259F%25E5%2581%25A5%25E5%25BA%25B7%25E5%25B1%2580%26phonumber%3D38f081fd68ce405dc77ad68aecd00e4c%26appId%3D006429D4E0%26userCert%3D9b7f802475421a4436c081967da51ba043da81fae7587d7a%26subMatter%3D1%26timestamp%3D1602576836398%26userName%3D%25E6%259D%25A8%25E5%2585%2589%25E5%2586%259B%26areaId%3D440103%26pf%3D4%26taskName%3D%25E5%258C%25BB%25E5%25B8%2588%25E6%2589%25A7%25E4%25B8%259A%25E8%25AF%2581%25E4%25B9%25A6%25EF%25BC%2588%25E5%258F%2598%25E6%259B%25B4%25EF%25BC%2589%26projectId%3D11440103007493637K4440120012002202009250310%26taskId%3D11440103007493637K4440120012002%26deptCode%3D11440103007493637K%26proManager%3D%25E8%2591%25A3%25E5%25AE%2581%26proManagerNo%3D11191'.encode())
sendBytes = client.send('HAOCHAPING?jsonpcallback=jQuery111105298489809635909_1602576785453&TYPE=http%3A%2F%2Fwww.baidu.com%3Fevaluatereq%2Fpad%2Fscore%3FacceptDate%3D2020-09-25%252009%3A32%3A39%26certType%3D10%26SBLSH%3Dlw0074936372009250297513%26proDepartId%3D007493637%26proStatus%3D%25E5%258A%259E%25E7%25BB%2593%26sign%3D459eb3ce196dc815f8996bf1baa76c2c%26resultDate%3D2020-10-13%252015%3A16%3A15%26hallCode%3D23144327010058265%26taskType%3D2%26areaName%3D%25E8%258D%2594%25E6%25B9%25BE%25E5%258C%25BA%26proDepart%3D%25E8%258D%2594%25E6%25B9%25BE%25E5%258C%25BA%25E5%258D%25AB%25E7%2594%259F%25E5%2581%25A5%25E5%25BA%25B7%25E5%25B1%2580%26phonumber%3D38f081fd68ce405dc77ad68aecd00e4c%26appId%3D006429D4E0%26userCert%3D9b7f802475421a4436c081967da51ba043da81fae7587d7a%26subMatter%3D1%26timestamp%3D1602576836398%26userName%3D%25E6%259D%25A8%25E5%2585%2589%25E5%2586%259B%26areaId%3D440103%26pf%3D4%26taskName%3D%25E5%258C%25BB%25E5%25B8%2588%25E6%2589%25A7%25E4%25B8%259A%25E8%25AF%2581%25E4%25B9%25A6%25EF%25BC%2588%25E5%258F%2598%25E6%259B%25B4%25EF%25BC%2589%26projectId%3D11440103007493637K4440120012002202009250310%26taskId%3D11440103007493637K4440120012002%26deptCode%3D11440103007493637K%26proManager%3D%25E8%2591%25A3%25E5%25AE%2581%26proManagerNo%3D11191'.encode())
#recvData = client.recv(MaxBytes)
#localTime = time.asctime( time.localtime(time.time()))
#print(localTime, ' 接收到数据字节数:',len(recvData))
#print(recvData.decode())
client.close()