#coding=utf-8

import urllib2

import threading

import time

 

TOTAL = 0 #����  

SUCC = 0 #��Ӧ�ɹ���  

FAIL = 0 #��Ӧʧ����  

EXCEPT = 0 #��Ӧ�쳣��  

MAXTIME=0 #�����Ӧʱ��  

MINTIME=100 #��С��Ӧʱ�䣬��ʼֵΪ100��

# ���໯Thread

class Mythread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def getResult(self):
        return self.res

    def run(self):
        self.res = apply(self.func, self.args)

def request_url(url, r):
    global TOTAL  
    global SUCC  
    global FAIL  
    global EXCEPT
    try:
        st = time.time()
        params = "{\"interfacename\":\"getcounterinfo\",\"counterno\":\"1\"}" # urllib.urlencode(params)
        req = urllib2.Request(url, params)    #����ҳ���������������
        response = urllib2.urlopen(req)     #����ҳ������
        print response.read()    #��ȡ���������ص�ҳ����Ϣ
        status = response.getcode()
        print status
        if status == 200:
            TOTAL+=1  
            SUCC+=1  
        else:
            TOTAL+=1  
            FAIL+=1
        time_span = time.time()-st 
        maxtime(time_span)
        self.mintime(time_span) 
    except Exception, e:
        TOTAL+=1  
        EXCEPT+=1
 
def maxtime(ts):  
    global MAXTIME  
    if ts>MAXTIME:  
        MAXTIME=ts  

def mintime(ts):  
    global MINTIME  
    if ts<MINTIME:  
         MINTIME=ts
 

def main():
    print '===========task start==========='  
    # ��ʼ��ʱ��  
    start_time = time.time()  
    # �������߳���  
    thread_count = 10
    i = 0  
    while i < thread_count:  
        t = Mythread(request_url, ('http://192.168.1.103:8083/queueSysinterface.aspx', "x"))
        t.start()
        i += 1
    t=0  
    #���������ж���ɻ����20��ͽ���  

    while TOTAL<thread_count|t>2:  

        print "total:%d,succ:%d,fail:%d,except:%d\n"%(TOTAL,SUCC,FAIL,EXCEPT)  

        t+=1  

        time.sleep(1)

 

    print '===========task end==========='  

    print "total:%d,succ:%d,fail:%d,except:%d"%(TOTAL,SUCC,FAIL,EXCEPT)  

    print 'response maxtime:',MAXTIME  

    print 'response mintime',MINTIME

    s = raw_input("Press any key")

    print "bay!"

    pass

 

if __name__ == "__main__":

    main()
