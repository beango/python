#-*- coding: UTF-8 -*-
#!/usr/bin/env python
#coding=utf-8 
import ctypes
import sys
import os
import hashlib
from PyQt4 import QtGui,QtWebKit
from pyDes import *

Version = 0.1
encrypted_flag = False#初始状态为加密方向
byteMd5 = lambda b:hashlib.new('md5',b).digest()
p = lambda s:ctypes.c_char_p(s)

def trans():
    global encrypted_flag
    print('*'*50)

    text_str = user_text.toPlainText()
    text_str = pre_process(text_str)
    print('len = %d,text = %s'%(len(text_str),text_str))

    key_str = key.text()
    print('key = ',key_str)

    if encrypted_flag:
        encrypted_flag = False
        ret = decrypt_string(text_str,key_str)
    else:    
        encrypted_flag = True
        ret = ""
        ret = encrypt_string(text_str,key_str)

    user_text.setPlainText(ret)

def refresh_gui():
    global trans_button,encrypted_flag 
    
    encrypted_flag = False
    msg_str = user_text.toPlainText()
    msg_str = pre_process(msg_str)
    
    if judge_encrypted(msg_str) == True:
        encrypted_flag = True
        trans_button.setText(u'解密')
    else:
        encrypted_flag = False
        trans_button.setText(u'加密')

#判断当前文本是否经过加密
def judge_encrypted( msg_str ):
    try:
        encrypt_bytes = viewableToBytes(msg_str)
    except:
        return False
    
    #是否达到最小长度
    if len(encrypt_bytes) < 8 + 8 + 1 + 4:
        return False
        
    md5_tail = encrypt_bytes[-4:]#md5(1)
    encrypt_bytes = encrypt_bytes[:-4]
    
    if byteMd5(encrypt_bytes)[-4:] == md5_tail:
        return True
    else:
        return False

def viewableToBytes(viewableStr):
    print('viewable str len = %d'%len(viewableStr))

    if len(viewableStr)%2 != 0:
        raise Exception("数据长度不为2的整数倍")

    count = 0
    b = bytearray(int(len(viewableStr)/2))
    
    for count in range(int(len(viewableStr)/2)):
        #print(viewableStr[count:count+2])
        b[count] = int(viewableStr[count*2:count*2+2] ,base = 16)

    print('unviewable bytes len = %d'%len(b))
    print(b)
    
    return bytes(b)

#bytes转化为hex格式
def bytesToViewable(b):
    print('unviewable bytes len = %d'%len(b))
    print(b)

    viewableStr = ''
    count = 0
    for byte in b:
        #print(byte)
        s = hex(byte)[2:].upper()
        if len(s) == 1:
            viewableStr += '0' + s
        else:
            viewableStr += s

    print('viewable str len = %d'%len(viewableStr))
    
    return viewableStr 

def pre_process(s):
    #去掉末尾的空格,回车...
    if len(s) == 0:
        return ""

    while True:
        if s[-1] == ' ':
            s = s[:-1]
            print('i')
        elif s[-1] == '\r':
            s = s[:-1]
            print('j')
        elif s[-1] == '\n':
            s = s[:-1]
            print('k')
        else:
            break

    return s

#加密长度为8整数倍的bytes
#msg_b,key 为 bytes类型
#返回相同长度加密之后的bytes
def encrypt_bytes(msg_b,key):

    global Objdll
    if len(msg_b)%8 !=0:#需要填充为8字节的整数倍
        raise Exception("数据长度不为8的整数倍") 
    
    print('before encrypt bytes,len = ',len(msg_b))
    tmp_raw = ctypes.create_string_buffer(len(msg_b))

    ret = Objdll.DES_Encrypt_Data(p(msg_b),p(key),tmp_raw,ctypes.c_int(len(msg_b)))
    
    print('after encrypt bytes,len = ',len(tmp_raw.raw))
    print(tmp_raw.raw)
    
    #print('ret = ',ret)
    
    return tmp_raw.raw

#根据传入的key来加密str_plain
#返回加密之后的str_plain
#处理str_plain编码,长度补全,并计算key的md5作为密钥
#在尾部附加 补全长度 标记和校验信息
#返回加密之后的str_plain
def encrypt_string(str_plain,key):
    print('before encrypt string,str len = ',len(str_plain))
    text_bytes = str_plain.toUtf8()
    key_bytes = key.toUtf8()
    
    if(len(text_bytes) == 0  or len(text_bytes) == 0):
        return
    
    key_md5 = byteMd5(key_bytes)
    print('key_md5 = ',key_md5)
    print('before encrypt string,bytes len = ',len(text_bytes))
        
    #补全长度为8的整数倍
    if len(text_bytes)%8 !=0:#需要填充为8字节的整数倍
        tail_len = 8 - len(text_bytes)%8
        text_bytes += b' ' * tail_len
    else:
        tail_len = 0

    md5_2 = byteMd5(text_bytes)[-8:]
    text_bytes += md5_2

    ret = encrypt_bytes(text_bytes,key_md5)
    
    print('after encrypt string,bytes len = ',len(ret))

    #在加密数据的尾部附加填充长度信息
    tmp = bytearray(1)
    tmp[0] = tail_len
    ret += bytes(tmp)

    #尾部附加md5(1)的后四位作为校验信息
    ret += byteMd5(ret)[-4:]
    
    return bytesToViewable(ret)

Objdll = ctypes.cdll.LoadLibrary("des_X2")

app = QtGui.QApplication(sys.argv)
windows_main = QtGui.QWidget()#主窗口
windows_main.setWindowTitle(u"文本加密工具 V" + "%s"%Version + " By HD")
windows_main.resize(500,250)

layout_main = QtGui.QVBoxLayout()
layout_up = QtGui.QHBoxLayout()
layout_down = QtGui.QHBoxLayout()

layout_down.setMargin(0)

key_label = QtGui.QLabel(u"口令")
key = QtGui.QLineEdit()
trans_button = QtGui.QPushButton(u"加密")
user_text = QtGui.QTextEdit()
layout_up.addWidget(key_label)
layout_up.addWidget(key)
#layout_up.addStretch(1)
layout_up.addWidget(trans_button)

layout_down.addStretch(1)

layout_main.addLayout(layout_up)
layout_main.addWidget(user_text)  
layout_main.addLayout(layout_down)

windows_main.setLayout(layout_main)

trans_button.clicked.connect(trans)
user_text.textChanged.connect(refresh_gui)

windows_main.show()
sys.exit(app.exec_())