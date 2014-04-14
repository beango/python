#!/usr/bin/env python
# -*- coding: utf-8 -*-
# test.py
#
# python高级程序

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

'''
#def 也可以有end
'''
__builtins__.end = None

def main():
	print 'def也可以有end'
end

main()


'''
设置全局变量
'''

d = {'a': 1, 'b':2}
for v,k in d.iteritems():# 粗暴的写法
	print v, '=', k

#print locals()
globals().update(d)
#print globals()

assert a==1
assert b==2
assert globals()['a']==1

globals()['a']==2
globals().update(d)

assert globals()['a']==1
assert d['a']==1

d['a']=2
assert globals()['a']==1
globals().update(d)
assert globals()['a']==2
assert d['a']==2
#assert globals()['a']==2

'''
字符串格式化
'''
print '{key}={val}'.format(key='a', val='123')
print '[{0:<10}][{0:^10}][{0:*>10}]'.format('hello')