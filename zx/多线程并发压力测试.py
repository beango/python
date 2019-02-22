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
                filename='���Խű���־.log',
                filemode='w')

def log_uncaught_exceptions(exception_type, exception, tb):
    logging.critical(''.join(traceback.format_tb(tb)))
    logging.critical('{0}: {1}'.format(exception_type, exception))

sys.excepthook = log_uncaught_exceptions

#���ص�ַ
url='http://192.168.1.103:8083/queueSysinterface.aspx'
thread_count = 1 #���β�������
requst_interval = 0.001 #������(��)
test_count = 10000 #sys.maxsize  # ָ�����Դ���

islog = False
now_count = 0
lock_obj = thread.allocate()
def send_http():
    global url
    global islog
    httpClient = None
    try:
        params = "{\"interfacename\":\"getcounterinfo\",\"counterno\":\"1\"}" # urllib.urlencode(params)
        req = urllib2.Request(url, params)    #����ҳ���������������
        response = urllib2.urlopen(req)     #����ҳ������
        
        if islog:
            #print '��������: ' + params
            print '������: ' + str(response.getcode())
            #print '��������: ' + response.read()

            logging.info('��������: ' + params)
            logging.info('������: ' + str(response.getcode()))
            logging.info('��������: ' + response.read())
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
        #print '���ʱ��'+str(requst_interval)

        if islog:
            print ''
            print '***************************�������:' + str(cnt) + "---now_count:" + str(now_count) + '*******************************'
            print 'Thread:(%d) Time:%s\n'%(thread.get_ident(), time.ctime())

            logging.info(' ')
            logging.info('***************************�������:' + str(cnt) + '*******************************')
            logging.info('Thread:(%d) Time:%s\n'%(thread.get_ident(), time.ctime()))
            sys.stdout.flush()

        cnt+=1
        now_count+=1
        send_http()
        lock_obj.release()
        time.sleep(0.001)

def test(ct):
    thread_count
    print('�߳���'+ str(thread_count) + ', ������:'+str(ct))
    sys.stdout.flush()
    for i in range(thread_count):
        thread.start_new_thread(test_func,(ct,))

if __name__=='__main__':
    test_count
    thread_count
    test(test_count)
    while now_count<test_count*thread_count:
        time.sleep(0.1)