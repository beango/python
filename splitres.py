#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
f = open('2.txt', 'r')  
fr = f.read().split(',')
wfile=open('22.txt','w')

print len(fr)
print fr[0]

index = 0
i = 0
rst = ""
while (index < len(fr)):
   rst += fr[index]+","
   if i==1000:
       wfile.write(rst)
       wfile.write('\n')
       rst = ""
       i = 0
   i = i+1
   index = index + 1
wfile.write(rst)
print len(fr)
'''

'''
f = open('20.txt', 'r')  
f2 = open('21.txt', 'r')  
while 1:
    line = f.readline()
    if not line:
        break

    while 1:
        line2 = f2.readline()
        #print line, line2
        if not line2:
            print 1,line
            break
        if line == line2:
            # print 2,line
            break;
        #print line
    #break
    
'''


f1 = open('20.txt', 'r')  
f1s = f1.read().split(',')

f2 = open('21.txt', 'r')  
f2s = f2.read().split(',')

print len(f1s)
print len(f2s)
print len(list(set(f1s)))
print list(set(f2s) ^ set(f1s))
