#!/usr/bin/env python
# -*- coding: utf-8 -*-
# test.py
#
# 两种不同的多线程处理方式

import Queue
import threading, thread, time, logging, datetime
from multiprocessing.dummy import Pool as ThreadPool  

class poolcls(threading.Thread):
    def __init__(self,_q):
        threading.Thread.__init__(self)
        self._task_queue = _q
    def run(self):
        while True:
            _task = self._task_queue.get()

            _func = _task.get("m")
            _arg = _task.get("arg")
            _sleep = _task.get("sleep")
            _cb = _task.get("callback")
            if _arg == "exit":
                break
            print "I'm a thread, and I received %s!!" % _arg
            if _cb :
                _cb(_arg)

def handle_result(result):
    print(type(result), result)

def p(_arg):
    time.sleep(_arg)
    print "I'm a thread2, and I received %s!!" % _arg,datetime.datetime.now()

def main():
    q = Queue.Queue()
    worker = poolcls(q)
    worker.start()
    start_time = time.time() 
    # While under 5 seconds.. 
    while time.time() - start_time < 5:
        q.put({'arg':datetime.datetime.now(), 'sleep':2.8, 'callback' : handle_result})
        time.sleep(1)

    q.put({'arg':"exit"})
    worker.join()

def main1():
    t = ThreadPool(4)
    result = t.map(p,[1,2,3,4])

    t.close()
    t.join()

import multiprocessing

def main2():
    jobs = []
    procs = 4
    for i in range(0, procs):
        out_list = list()
        process = multiprocessing.Process(target=p, 
                                          args=([1+i]))
        jobs.append(process)

    # Start the processes (i.e. calculate the random number lists)    
    for j in jobs:
        j.start()
 
    # Ensure all of the processes have finished
    for j in jobs:
        j.join()
 
    print "List processing complete."

import sys
sys.path.append("..")
from module.timer import Timer

if __name__ == "__main__":
    with Timer() as t:
        main1()
    print "=> elasped lpush: %s s" % t.secs
