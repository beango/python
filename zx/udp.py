#!/usr/bin/python2.6  
# -*- coding: utf-8 -*-  

import socket,sys,re
import os

devices = os.popen("adb devices -l | sed '1d' | sed '/./!d'").readlines()
if len(devices) > 1:
    remodel = re.compile("^(.*)device.*model:(.*)device.*$")
    def read_a_target(max):
        print 'Target:',
        try:
            var = raw_input()
        except KeyboardInterrupt:
            sys.stdout.flush()
            exit(1)
        try:
            var = int(var)
            if 0 <= var <= max:
                return var
            return read_a_target(max)
        except Exception, _:
            print read_a_target(max)
    print 'Select the target device: '
    for i in range(len(devices)):
        res = remodel.match(devices[i])
        if res:
            id, model = res.groups()
            print '[%d]: %s -> %s' % (i, id.strip().upper(), model.strip())
        else:
            tmparr = re.compile("\\s+").split(devices[i])
            print '[%d]: %s -> %s' % (i, tmparr[0].upper(), tmparr[1])
    target = read_a_target(len(devices) - 1)
    res = remodel.match(devices[target])
    if res:
        id, model = res.groups()
        print id.strip()
    else:
        tmparr = re.compile("\\s+").split(devices[target])
        print 'The target is %s' % tmparr[1]
        exit(0)

#os.popen("adb forward tcp:8000 tcp:9002")

address = ('192.168.1.111', 8001)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#s.sendto("00411", address)

s.sendto("S01||E", address) #��ӭ����
#s.sendto("S02", address) #����
#s.sendto("S03", address) #��ͣ
#s.sendto("S041001E", address) #��¼
#s.sendto("S05", address) #�˳�
#s.sendto("S06", address) #ȡ������
#s.sendto("S071001E", address)
#s.sendto("S04||1001||E", address)
#s.sendto("PT", address)
#s.sendto("S50||11||0E", address)

s.close()