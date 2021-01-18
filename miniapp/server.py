#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by huangding 2017/7/9

from flask import Flask, request, Response, make_response
import json
import time
import arrow
import os
import soup
from apscheduler.schedulers.background import BackgroundScheduler

# Flask初始化参数尽量使用你的包名，这个初始化方式是官方推荐的，官方解释：http://flask.pocoo.org/docs/0.12/api/#flask.Flask
app = Flask(__name__)


@app.route('/add')
def add():
    d = []
    type = request.args.get("type")
    value = request.args.get("value")

    if os.path.exists('static/add.json'):
        f = open('static/add.json', encoding='utf-8')
        res = f.read()
        d = json.loads(res)
        for item in d:
            if(item["type"] == type and item["value"] == value):
                return "OK"

    # d.remove(item)
    d.append({'type': type, 'value': value})
    fw = open('./static/add.json', 'w', encoding='utf-8')
    json.dump(d, fw, ensure_ascii=False, indent=2)
    return "OK"


@app.route('/daily')
def daily():
    f = open('./static/daily2.json', encoding='utf-8')
    res = f.read()
    return Response(json.dumps(json.loads(res), ensure_ascii=False),  mimetype='application/json;charset=UTF-8')


@app.route('/getfb')
def getfb():
    fbname = request.args.get("name")
    print(fbname)
    f = open('./static/stages/'+fbname+'.json', encoding='utf-8')
    res = f.read()
    return Response(json.dumps(json.loads(res), ensure_ascii=False),  mimetype='application/json;charset=UTF-8')


@app.route('/syncrecent')
def syncrecent():
    print(len(scheduler.get_jobs()))
    if len(scheduler.get_jobs()) > 0:
        return "还有其他任务"
    nowstr = arrow.get().to('local').shift(seconds=2).format("YYYY-MM-DD HH:mm:ss")
    scheduler.add_job(task_recent, 'date', run_date=nowstr)
    return "OK%d" % len(scheduler.get_jobs())


def addtask():
    if os.path.exists('static/add.json'):
        f = open('static/add.json', encoding='utf-8')
        res = f.read()
        d = json.loads(res)
        for item in d:
            print(item["type"], item["value"])
            if item["type"] == "skill" or item["type"] == "lskill":
                soup.getskill(item["value"])
                if os.path.exists('static/skill/'+item["value"]+'.json'):
                    d.remove(item)
        fw = open('./static/add.json', 'w', encoding='utf-8')
        json.dump(d, fw, ensure_ascii=False, indent=2)
    else:
        print('no file')

@app.route('/synczhs')
def synczhs():
    print(len(scheduler.get_jobs()))
    if len(scheduler.get_jobs()) > 0:
        return "还有其他任务"
    nowstr = arrow.get().to('local').shift(seconds=2).format("YYYY-MM-DD HH:mm:ss")
    scheduler.add_job(task_zhs, 'date', run_date=nowstr, args=['text'])
    return "OK"


def clear():
    fw = open('static/log.txt', 'w', encoding='utf-8')
    fw.truncate()  # 清空文件
    fw.close()


def updatezhs():
    obj = soup.TestClass()
    obj.getallzhs('1-300')
    obj.getallzhs('301-600')
    obj.getallzhs('601-900')
    obj.getallzhs('901-1200')
    obj.getallzhs('1201-1500')
    obj.getallzhs('1501-1800')
    obj.getallzhs('1801-2100')
    obj.getallzhs('2101-2400')
    obj.getallzhs('2401-2700')
    obj.getallzhs('其它A-Z')
    obj.mergeallzhs()  # 将所有资料合并到zhsseries.json


def task_recent():
    starttime = arrow.get()
    msg = "开始更新最近关卡: %s" % starttime.to('local').format()
    print(msg)
    fw = open('static/log.txt', 'r+', encoding='utf-8')
    content = fw.read()
    fw.seek(0, 0)
    fw.write(msg)
    fw.write('\n')
    fw.write(content)
    fw.close()

    soup.getrecentimg()
    soup.getrecent()
    soup.getrecenttask()

    endtime = arrow.get()
    msg = "最近关卡更新完成: %s, 花费时间：%d秒" % (endtime.to(
        'local').format(), endtime.timestamp-starttime.timestamp)
    fw = open('static/log.txt', 'r+', encoding='utf-8')
    content = fw.read()
    fw.seek(0, 0)
    fw.write(msg)
    fw.write('\n')
    fw.write(content)
    fw.close()


def task_zhs(text):
    starttime = arrow.get()
    msg = "开始更新所有召唤兽: %s" % starttime.to('local').format()
    fw = open('static/log.txt', 'a+', encoding='utf-8')
    fw.write(msg)
    fw.write('\n')
    fw.close()

    soup.getallzhs('1-300')
    soup.getallzhs('301-600')
    soup.getallzhs('601-900')
    soup.getallzhs('901-1200')
    soup.getallzhs('1201-1500')
    soup.getallzhs('1501-1800')
    soup.getallzhs('1801-2100')
    soup.getallzhs('2101-2400')
    soup.getallzhs('2401-2700')
    soup.getallzhs('其它A-Z')

    endtime = arrow.get()
    msg = "召唤兽更新完成: %s, 花费时间：%d秒" % (endtime.to(
        'local').format(), endtime.timestamp-starttime.timestamp)
    fw = open('static/log.txt', 'a+', encoding='utf-8')
    fw.write(msg)
    fw.write('\n')
    fw.close()

# if __name__ == "__main__":
# $ export FLASK_APP=/home/server.py
# $ flask run --host=0.0.0.0 >null 2>&1 &
#     app.config['JSON_AS_ASCII'] = False

# task_recent()

scheduler = BackgroundScheduler()
scheduler.add_job(clear, 'cron', day_of_week='0-6',
                  hour=0, minute=0, second=0)  # 定时更新最近关卡
scheduler.add_job(task_recent, 'interval', minutes=5)  # 定时更新最近关卡
# scheduler.add_job(updatezhs, 'interval', hours=2) #定时更新zhs
# scheduler.add_job(addtask, 'interval', minutes=1) #补漏
scheduler.start()

# app.run(host='0.0.0.0', port='5000', debug=True)
app.run(host='0.0.0.0', port='443', debug=False, ssl_context='adhoc')
