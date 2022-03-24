#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by huangding 2017/7/9

import arrow
import soup

def writelog(msg):
    fw = open('static/log.txt', 'r+', encoding='utf-8')
    content = fw.read()
    fw.seek(0, 0)
    fw.write(msg)
    fw.write('\n')
    fw.write(content)
    fw.close()

starttime = arrow.get()
msg = "开始更新最近关卡: %s" % starttime.to('local').format()
writelog(msg)

soup.getalltc()
soup.getrecentimg()
soup.getrecent()
soup.getrecenttask()

endtime = arrow.get()
msg = "最近关卡更新完成: %s, 花费时间：%d秒" % (endtime.to(
        'local').format(), endtime.timestamp-starttime.timestamp)
writelog(msg)