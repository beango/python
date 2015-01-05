#!/usr/bin/env python
# coding: utf-8
#
#
# show time in console
#
import sys
import time
 
raws = '''
.--.
|  |
|  |
|  |
`--`
  .
 /|
  |
  |
 ---
---.
   |
---`
|
`---
---.
   |
---|
   |
---`
.  .
|  |
`--|
   |
   |
.---
|
`--.
   |
---`
.---
|
|--.
|  |
`--`
.--.
|  |
`  |
   |
   |
.--.
|  |
|--|
|  |
`--`
.--.
|  |
`--|
   |
---`
'''.strip()
numbers = {}
def init():
    for num in range(10):
        numbers[str(num)] = []
    lineno = 0
    for line in raws.split('\n'):
        line = line.ljust(4)
        arr = []
        for char in line:
            arr.append(char) # != ' ')
        numbers[str(lineno/5)].append(arr)
        lineno += 1
    numbers[':'] = [[' ', ' ', ' ', ' '], [' ', ' ', '-', ' '], [' ', ' ', ' ', ' '], [' ', ' ', '-', ' '], [' ', ' ', ' ', ' ']]
    numbers[' '] = [[' ', ' ', ' ', ' '], [' ', ' ', ' ', ' '], [' ', ' ', ' ', ' '], [' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ']]
def print_num(digtal):
    digtal = str(digtal)
    screen = []
    for i in range(5):
        screen.append([])
    for num in digtal:
        for i, linechar in enumerate(numbers[num]):
            for char in linechar:
                screen[i].append(char)
            screen[i].append('   ')
    for line in screen:
        print ''.join(line)
init()
def cls():
    sys.stdout.write('\033[2J\033[0;0H')
    sys.stdout.flush()
 
while True:
    t = time.strftime("%H:%M:%S")
    cls(); print_num(t)
    time.sleep(1)
    t = time.strftime("%H %M %S")
    cls(); print_num(t)
    time.sleep(1)