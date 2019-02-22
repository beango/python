#!/usr/bin/env python
#coding:UTF-8

"""
  Author: jefferchen@163.com
  可在命令行直接带目的IP，也可将IP列表在文本文件中。
  pingip.py -d DestIP 
  DestIP示例： a)单个： 192.168.11.1
               b)多个:  192.168.11.1;172.16.8.1;176.13.18.2
               c)网段:  192.168.11.1-127
    文本文件：ip.txt
            目的IP多行存储
"""

import argparse
import os
import platform
import time,datetime

def PingCmd():
    cmdStr = ''
    if platform.system()=='Linux':
        cmdStr = 'ping -c 1 %s > /dev/null'
    else:
        cmdStr =  'ping -n 1 %s > nul'
    return cmdStr

def IPV4SegList(aList):
    IPSeg = aList[0].split('.')
    IP4Begin = int(IPSeg[3])
    IP4End   = int(aList[1])
    segList = []
    if IP4End<=IP4Begin:
        IP4End  += IP4Begin
    else:
        IP4End +=1
    for ip in range(IP4Begin,IP4End):
        aIP = IPSeg[0]+'.'+IPSeg[1]+'.'+IPSeg[2]+'.'+str(ip)
        segList += [aIP]
    return  segList

def ParseSeg(aSeg):
    segList = []
    aList = aSeg.split('-')
    if len(aList)==2:
        segList = IPV4SegList(aList)
    else:
        segList = aList
    return segList

def AddLineIP(IPList,aLine):
    LineList = aLine.split(';')
    for aSeg in LineList:
        segList = ParseSeg(aSeg)
        IPList += segList
    return IPList

def GetIPListFromFile(filename):
    IPList = []
    f = open(filename)
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        line = line.replace('\n','')
        IPList = AddLineIP(IPList,line)
    return IPList

def NotifyAdmin(failureIP):
    print('Network error at ',failureIP)

def ReportSummary(success,failure):
    print('----DONE! Total: %s nodes. %s ---'%(success+failure,timeFmt()))

def PingList(aList):
    sucess,failure = 0,0
    failureIP = []
    print('Trying...')
    for ip in aList:
        cmdStr = PingCmd()%ip.replace('\n','')
        res = os.system(cmdStr)
        if res < 1 :
            sucess += 1
        else:
            failure += 1
            failureIP += [ip]
        time.sleep(1)
    if failure :
         NotifyAdmin(failureIP)
    else:
        ReportSummary(sucess,failure);


def timeFmt():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

def writeLog(content):
    print('[%s] %s' % (timeFmt(), content))
    file_object = open('ping.' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log', 'a')
    file_object.write('[%s] %s\n' % (timeFmt(), content));
    file_object.close()

if __name__ == '__main__':
    parse = argparse.ArgumentParser(description='Batch ping utility.')
    parse.add_argument('-f','--filename',default='ip.txt',help='IP file name(Default IP.txt)')
    parse.add_argument('-d','--destip',type=str,default='',help='destination IPs ');
    args = parse.parse_args()
    if args.destip!='':
        IPList = AddLineIP([],args.destip)
    else:
        if args.filename!='':
            IPFile = args.filename
        else:
            IPFile = 'ip.txt'
        IPList = GetIPListFromFile(IPFile)

    PingList(IPList)