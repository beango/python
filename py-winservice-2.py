#!/usr/bin/env python
# -*- coding: utf-8 -*-
# SmallestService.py
#
# A sample demonstrating the smallest possible service written in Python.
"""
安装服务　　　　python PythonService.py install 
自动启动　　　　python PythonService.py --startup auto install 
启动服务　　　　python PythonService.py start 
重启服务　　　　python PythonService.py restart
停止服务　　　　python PythonService.py stop
删除/卸载服务　 python PythonService.py remove
"""
import win32serviceutil
import win32service
import win32event

class SmallestPythonService2(win32serviceutil.ServiceFramework):
    _svc_name_ = "PythonServiceDemo2"
    _svc_display_name_ = "PythonServiceDemo2"
    _svc_description_ = "Python service demo2."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        # Create an event which we will use to wait on.
        # The "service stop" request will set this event.
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.logger = self._getLogger()
        self.isAlive = True

    def _getLogger(self):
        import logging
        import os
        import inspect
        
        logger = logging.getLogger('[PythonService2]')
        
        this_file = inspect.getfile(inspect.currentframe())
        dirpath = os.path.abspath(os.path.dirname(this_file))
        handler = logging.FileHandler(os.path.join(dirpath, datetime.date.today().strftime('%Y%m%d')+"-2.log"))
        
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        return logger

    def SvcStop(self):
        # 先告诉SCM停止这个过程 
        self.logger.error("svc2 do stop....")
        # Before we do anything, tell the SCM we are starting the stop process.
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # And set my event.
        win32event.SetEvent(self.hWaitStop)
        self.isAlive = False

    def SvcDoRun(self):
        import time
        self.logger.info("svc2 do run....") 
        while self.isAlive:
            self.logger.info("I am alive. demo2")
            time.sleep(7)
        # We do nothing other than wait to be stopped!
        #win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

if __name__=='__main__':
    win32serviceutil.HandleCommandLine(SmallestPythonService2)