#!/usr/bin/python2.6  
# -*- coding: utf-8 -*-  
import sys,time,random,types
import socket,os,struct
reload(sys)
sys.setdefaultencoding('utf8')

from socket import *

_MAPPING = (u'零', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九', )
_P0 = (u'', u'十', u'百', u'千', )
_S4, _S8, _S16 = 10 ** 4 , 10 ** 8, 10 ** 16
_MIN, _MAX = 0, 9999999999999999

def _to_chinese4(num):
  '''转换[0, 10000)之间的阿拉伯数字
  '''
  assert(0 <= num and num < _S4)
  if num < 10:
    return _MAPPING[num]
  else:
    lst = [ ]
    while num >= 10:
      lst.append(num % 10)
      num = num / 10
    lst.append(num)
    c = len(lst)  # 位数
    result = u''
    
    for idx, val in enumerate(lst):
      if val != 0:
        result += _P0[idx] + _MAPPING[val]
        if idx < c - 1 and lst[idx + 1] == 0:
          result += u'零'
    
    return result[::-1].replace(u'一十', u'十')
    
def _to_chinese8(num):
  assert(num < _S8)
  to4 = _to_chinese4
  if num < _S4:
    return to4(num)
  else:
    mod = _S4
    high, low = num / mod, num % mod
    if low == 0:
      return to4(high) + u'万'
    else:
      if low < _S4 / 10:
        return to4(high) + u'万零' + to4(low)
      else:
        return to4(high) + u'万' + to4(low)
      
def _to_chinese16(num):
  assert(num < _S16)
  to8 = _to_chinese8
  mod = _S8
  high, low = num / mod, num % mod
  if low == 0:
    return to8(high) + u'亿'
  else:
    if low < _S8 / 10:
      return to8(high) + u'亿零' + to8(low)
    else:
      return to8(high) + u'亿' + to8(low)
    
def to_chinese(num):
  if type(num) != types.IntType and type(num) != types.LongType:
    raise NotIntegerError(u'%s is not a integer.' % num)
  if num < _MIN or num > _MAX:
    raise OutOfRangeError(u'%d out of range[%d, %d)' % (num, _MIN, _MAX))
  
  if num < _S4:
    return _to_chinese4(num)
  elif num < _S8:
    return _to_chinese8(num)
  else:
    return _to_chinese16(num)

# 1. 创建udp套接字
udp_socket = socket(AF_INET, SOCK_DGRAM)

# 2. 准备接收方的地址
# '192.168.1.103'表示目的ip地址
# 8080表示目的端口
dest_addr = ('192.168.1.114', 8001)
# 3. 从键盘获取数据
#D,0001,1,3,W,内儿科门诊,3002,黄宇,张*3,E
send_data = "S94STOPE" #S94STOPE - S94E
udp_socket.sendto(send_data.encode('gb2312'), dest_addr);
# 5. 关闭套接字
udp_socket.close()



filepath = 'C:/Users/Administrator/Pictures/19.jpg'
s = socket(AF_INET, SOCK_STREAM)
s.connect(('192.168.1.1', 8001))
fhead = struct.pack('128sl', os.path.basename(filepath), os.stat(filepath).st_size)
s.send(fhead)

fo = open(filepath,'rb')
while True:
	filedata = fo.read(1024)
	if not filedata:
		break
	s.send(filedata)
fo.close()
s.close()