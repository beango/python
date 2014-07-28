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

class SmallestPythonService(win32serviceutil.ServiceFramework):
    _svc_name_ = "PythonServiceDemo1"
    _svc_display_name_ = "PythonServiceDemo1"
    _svc_description_ = "Python service demo1."

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
        import datetime

        logger = logging.getLogger('[PythonService1]')
        
        this_file = inspect.getfile(inspect.currentframe())
        dirpath = os.path.abspath(os.path.dirname(this_file))
        handler = logging.FileHandler(os.path.join(dirpath, "log/%s-1.log" % datetime.date.today().strftime('%Y%m%d')))
        
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        return logger

    def SvcStop(self):
    	# 先告诉SCM停止这个过程 
        self.logger.error("svc1 do stop....")
        # Before we do anything, tell the SCM we are starting the stop process.
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # And set my event.
        win32event.SetEvent(self.hWaitStop)
        self.isAlive = False

    def SvcDoRun(self):
        import time
        from eve import Eve 
        self.logger.info("svc1 do run....") 
        while self.isAlive:
            self.logger.info("I am alive. demo1")
            c1(self.logger)
            time.sleep(10)
        # We do nothing other than wait to be stopped!
        #win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

class c1:
    def __init__(self, _logger):
        _logger.info("c1...")

if __name__=='__main__':
    win32serviceutil.HandleCommandLine(SmallestPythonService)