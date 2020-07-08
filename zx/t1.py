#coding=utf-8

import urllib2

import threading

import time

 

TOTAL = 0 #总数  

SUCC = 0 #响应成功数  

FAIL = 0 #响应失败数  

EXCEPT = 0 #响应异常数  

MAXTIME=0 #最大响应时间  

MINTIME=100 #最小响应时间，初始值为100秒

# 子类化Thread

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
        req = urllib2.Request(url, params)    #生成页面请求的完整数据
        response = urllib2.urlopen(req)     #发送页面请求
        print(response.read())   #获取服务器返回的页面信息
        status = response.getcode()
        print(status)
        if status == 200:
            TOTAL+=1  
            SUCC+=1  
        else:
            TOTAL+=1  
            FAIL+=1
        time_span = time.time()-st 
        maxtime(time_span)
        self.mintime(time_span) 
    except(Exception, e):
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
    print('===========task start==========='  )
    # 开始的时间  
    start_time = time.time()  
    # 并发的线程数  
    thread_count = 10
    i = 0  
    while i < thread_count:  
        t = Mythread(request_url, ('http://192.168.1.103:8083/queueSysinterface.aspx', "x"))
        t.start()
        i += 1
    t=0  
    #并发数所有都完成或大于20秒就结束  

    while TOTAL<thread_count|t>2:  

        print("total:%d,succ:%d,fail:%d,except:%d\n"%(TOTAL,SUCC,FAIL,EXCEPT))

        t+=1  

        time.sleep(1)

 

    print('===========task end===========')

    print ("total:%d,succ:%d,fail:%d,except:%d"%(TOTAL,SUCC,FAIL,EXCEPT)  )

    print ('response maxtime:',MAXTIME  )

    print ('response mintime',MINTIME)

    s = raw_input("Press any key")

    print ("bay!")

    pass

 

if __name__ == "__main__":

    main()
