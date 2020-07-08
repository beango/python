#coding=utf-8

import sys
import time
import thread
import httplib, urllib2
import random
import uuid
import logging
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='测试脚本日志.log',
                filemode='w')

def log_uncaught_exceptions(exception_type, exception, tb):
    #logging.critical(''.join(traceback.format_tb(tb)))
    logging.critical('{0}: {1}'.format(exception_type, exception))
    print tb

sys.excepthook = log_uncaught_exceptions

#网关地址
url='http://192.168.1.103:8083/queueSysinterface.aspx'
thread_count = 1 #单次并发数量
requst_interval = 0.001 #请求间隔(秒)
test_count = 10000 #sys.maxsize  # 指定测试次数

islog = False
now_count = 0
lock_obj = thread.allocate()
def send_http():
    global url
    global islog
    httpClient = None
    try:
        params = "{\"interfacename\":\"getcounterinfo\",\"counterno\":\"1\"}" # urllib.urlencode(params)
        req = urllib2.Request(url, params)    #生成页面请求的完整数据
        response = urllib2.urlopen(req)     #发送页面请求
        
        if islog:
            #print '发送数据: ' + params
            print '返回码: ' + str(response.getcode())
            #print '返回数据: ' + response.read()

            logging.info('发送数据: ' + params)
            logging.info('返回码: ' + str(response.getcode()))
            logging.info('返回数据: ' + response.read())
            sys.stdout.flush()
    except Exception, e:
        print e
        logging.info(e)
    finally:
        if httpClient:
            httpClient.close()

def test_func(run_count):
    global now_count
    global requst_interval
    global lock_obj
    global islog
    cnt = 0
    while cnt < run_count:
        lock_obj.acquire()
        #print '间隔时间'+str(requst_interval)

        if islog:
            print ''
            print '***************************请求次数:' + str(cnt) + "---now_count:" + str(now_count) + '*******************************'
            print 'Thread:(%d) Time:%s\n'%(thread.get_ident(), time.ctime())

            logging.info(' ')
            logging.info('***************************请求次数:' + str(cnt) + '*******************************')
            logging.info('Thread:(%d) Time:%s\n'%(thread.get_ident(), time.ctime()))
            sys.stdout.flush()

        cnt+=1
        now_count+=1
        send_http()
        lock_obj.release()
        time.sleep(0.001)

def test(ct):
    thread_count
    print('线程数'+ str(thread_count) + ', 请求数:'+str(ct))
    sys.stdout.flush()
    for _ in range(thread_count):
        thread.start_new_thread(test_func,(ct,))

if __name__=='__main__':
    test_count
    thread_count
    test(test_count)
    while now_count<test_count*thread_count:
        time.sleep(0.1)