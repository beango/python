#!/user/bin/env python
# -*- coding: UTF-8 -*-
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
            if _arg == "exit":
                break
            print "I'm a thread, and I received %s!!" % _arg

def main():
    q = Queue.Queue()
    worker = poolcls(q)
    worker.start()
    start_time = time.time() 
    # While under 5 seconds.. 
    while time.time() - start_time < 5:
        q.put({'arg':datetime.datetime.now(), 'sleep':2.8})
        time.sleep(1)

    q.put({'arg':"exit"})
    worker.join()

def p(_arg):
    time.sleep(_arg)
    print "I'm a thread2, and I received %s!!" % _arg,datetime.datetime.now()

def main1():
    t = ThreadPool(4)
    result = t.map(p,[1,2,3,4])

    t.close()
    t.join()

if __name__ == "__main__":
    main1()
