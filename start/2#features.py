#!/usr/bin/env python
# -*- coding: utf-8 -*-
# test.py
#
# 你可能不知道的 30 个 Python 语言的特点技巧

'''
分拆
'''
a,b,c = 1, 2, 3 
assert a == 1
assert b == 2
assert c == 3

a,b,c = [11, 12, 13] 
assert a == 11
assert b == 12
assert c == 13

a,b,c = (x*2+1 for x in range(3))
assert a == 1
assert b == 3
assert c == 5

'''
#交换变量
'''
a,b = 1,2 
a,b = b,a
assert a==2
assert b==1

