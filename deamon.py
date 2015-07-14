#coding=utf8

import threading
import time
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s]-(%(threadName)s)-%(message)s',
)

def worker():
    logging.debug('starting')
    #print 'I am worker:'
    time.sleep(2)
    logging.debug('ending')


def my_service():
    logging.debug('starting')
    #print 'I am service:'
    time.sleep(1)
    logging.debug('ending')

t = threading.Thread(name='worker-by leon',target=worker)
t.setDaemon(True) #False阻塞主进程，True不阻塞
t.start()
t.join(3) #等待守护线程退出,join的时间大于线程睡眠时间，所以isAlive()的值为False


d = threading.Thread(name='service-by leon', target=my_service)
d.setDaemon(True)
d.start()

logging.debug(t.isAlive())
d.join()
#不显示ending因为worker守护线程结束之前，主线程或其他线程已经退出
'''
显示
[DEBUG]-(worker-by leon)-starting
[DEBUG]-(worker-by leon)-ending
[DEBUG]-(MainThread)-False
[DEBUG]-(service-by leon)-starting
[DEBUG]-(service-by leon)-ending
'''