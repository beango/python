#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by huangding 2017/7/9

from flask import *
from flask_restful import Resource
import json, requests
import time
import arrow, socket
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
                return "已经存在"
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

def addtask():
    if os.path.exists('static/add.json'):
        f = open('static/add.json', encoding='utf-8')
        res = f.read()
        d = json.loads(res)
        if len(d)>0: print("____________________________________开始更新"); soup.getalltc();
        for item in d: 
            print(item["type"], item["value"])
            if item["type"] == "skill" or item["type"] == "lskill":
                soup.getskill(item["value"], "", True)
            if item["type"] == "zhs":
                soup.getzhs(item["value"], True)
            d.remove(item)
        fw = open('./static/add.json', 'w', encoding='utf-8')
        json.dump(d, fw, ensure_ascii=False, indent=2)
    else:
        print('no file')

def clear():
    fw = open('static/log.txt', 'w', encoding='utf-8')
    fw.truncate()  # 清空文件
    fw.close()


def updatezhs():
    starttime = arrow.get()
    msg = "开始更新召唤兽: %s" % starttime.to('local').format()
    writelog(msg)
    obj = soup.TestClass()
    obj.getteamskill()
    obj.getallzhs('1-300', False)
    obj.getallzhs('301-600', False)
    obj.getallzhs('601-900', False)
    obj.getallzhs('901-1200', False)
    obj.getallzhs('1201-1500', False)
    obj.getallzhs('1501-1800', False)
    obj.getallzhs('1801-2100', False)
    obj.getallzhs('2101-2400', False)
    obj.getallzhs('2401-2700', False)
    obj.getallzhs('其它A-Z', False)
    obj.mergeallzhs()
    endtime = arrow.get()
    msg = "召唤兽更新完成: %s, 花费时间：%d秒" % (endtime.to(
        'local').format(), endtime.timestamp-starttime.timestamp)
    writelog(msg)

def task_recent():
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

def writelog(msg):
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
    writelog(msg)

def task_test():
    url = "http://106.75.148.48:5000/question/pageList"
    res = requests.get(url, data={}, timeout=None, headers={"x-token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"})
    retdata = json.loads(res.content)
    # print(retdata)
    with open('static/data.json','w') as f:
        #写入方式1，等价于下面这行
        json.dump(retdata, f, ensure_ascii=False)

@app.route('/question/pageList')
def question_pageList():
    # return app.send_static_file('/root/static/ks.txt')
    url = "http://106.75.148.48:5000/question/pageList"
    # url = "http://localhost:5000/question/pageList"
    # return redirect('http://106.75.148.48:5000/question/pageList')
    res = requests.get(url, data={}, timeout=None, headers={"x-token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"})
    response = make_response(res.content)
    response.headers = dict(res.headers)
    return response

@app.route('/question/get')
def question_get():
    id = request.args.get("id")
    url = "http://106.75.148.48:5000/question/get?id=" + id
    
    # return redirect('http://106.75.148.48:5000/question/get?id=1')
    res = requests.get(url, data={}, timeout=None, headers={"x-token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"})
    response = make_response(res.content)
    for item in res.headers:
        print(item, res.headers[item])
        if item == "Content-Type": response.headers[item] = res.headers[item]
    # response.headers = dict(res.headers)
    return response

@app.route('/question/add', methods=['POST'])
def addQuestion():
    print(request.get_json())
    url = "http://106.75.148.48:5000/question/add"
    j = request.get_json()
    res = requests.post(url, data=json.dumps(j), timeout=None, headers={"x-token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"})
    response = make_response(res.content)
    response.headers = dict(res.headers)
    return response   

@app.route('/answer/add', methods=['POST'])
def question_answer():
    url = "http://106.75.148.48:5000/answer/add"
    j = request.get_json()
    res = requests.post(url, data=json.dumps(j), timeout=None, headers={"x-token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"})
    response = make_response(res.content)
    response.headers = dict(res.headers)
    return response

@app.route('/uploads/<imgname>', methods=['GET'])
def uploads(imgname):
    # return redirect("http://106.75.148.48:5000/uploads/" + imgname)
    url = "http://106.75.148.48:5000/uploads/" + imgname
    j = request.get_json()
    res = requests.get(url, timeout=None, headers={"x-token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"})
    response = make_response(res.content)
    response.headers = dict(res.headers)
    return response

@app.route('/static1/<imgname>', methods=['GET'])
def static1(imgname):
    # return redirect("http://106.75.148.48:5000/uploads/" + imgname)
    url = "http://106.75.148.48:5000/static/" + imgname
    # url = "http://localhost:5000/static/" + imgname
    j = request.get_json()
    res = requests.get(url, timeout=None, headers={"x-token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"})
    response = make_response(res.content)
    response.headers = dict(res.headers)
    return response


@app.route('/wx/login', methods=['GET'])
def wx_login():
    code = request.args.get("code")
    url = "http://106.75.148.48:5000/wx/login?code="+code
    res = requests.get(url, timeout=None, headers={"x-token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"})
    response = make_response(res.content)
    response.headers = dict(res.headers)
    return response

@app.route('/ks/login', methods=['GET'])
def ks_login():
    code = request.args.get("code")
    url = "http://106.75.148.48:5000/ks/login?code="+code
    res = requests.get(url, timeout=None, headers={"x-token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"})
    response = make_response(res.content)
    response.headers = dict(res.headers)
    return response

@app.route('/user/sync', methods=['POST'])
def user_sync():
    code = request.args.get("code")
    # return redirect("http://106.75.148.48:5000/uploads/" + imgname)
    url = "http://106.75.148.48:5000/user/sync"
    j = request.get_json()
    print(j)
    # j = {"wxOpenID":"123","userName":"123", "passWord":"123456" , "nickName": "123", "authorityId": "0", "deptId": 1}
    res = requests.post(url, data=json.dumps(j), timeout=None, headers={"x-token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"})
    response = make_response(res.content)
    response.headers = dict(res.headers)
    return response

@app.route('/user/kssync', methods=['POST'])
def user_kssync():
    code = request.args.get("code")
    # return redirect("http://106.75.148.48:5000/uploads/" + imgname)
    url = "http://106.75.148.48:5000/user/kssync"
    j = request.get_json()
    print(j)
    # j = {"wxOpenID":"123","userName":"123", "passWord":"123456" , "nickName": "123", "authorityId": "0", "deptId": 1}
    res = requests.post(url, data=json.dumps(j), timeout=None, headers={"x-token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"})
    response = make_response(res.content)
    response.headers = dict(res.headers)
    return response

@app.route('/user/setksuid', methods=['POST'])
def user_setksuid():
    code = request.args.get("code")
    # return redirect("http://106.75.148.48:5000/uploads/" + imgname)
    url = "http://106.75.148.48:5000/user/setksuid"
    j = request.get_json()
    print(j)
    # j = {"wxOpenID":"123","userName":"123", "passWord":"123456" , "nickName": "123", "authorityId": "0", "deptId": 1}
    res = requests.post(url, data=json.dumps(j), timeout=None, headers={"x-token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"})
    response = make_response(res.content)
    response.headers = dict(res.headers)
    return response

@app.route('/user/ks_setuid', methods=['POST'])
def ks_setuid():
    code = request.args.get("code")
    # return redirect("http://106.75.148.48:5000/uploads/" + imgname)
    url = "http://106.75.148.48:5000/user/ks_setuid"
    j = request.get_json()
    print(j)
    # j = {"wxOpenID":"123","userName":"123", "passWord":"123456" , "nickName": "123", "authorityId": "0", "deptId": 1}
    res = requests.post(url, data=json.dumps(j), timeout=None, headers={"x-token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"})
    response = make_response(res.content)
    response.headers = dict(res.headers)
    return response

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
isLocale = ip == "127.0.0.1"
if isLocale:
    scheduler = BackgroundScheduler()
    scheduler.add_job(task_test, 'interval', seconds=10)  # 定时更新最近关卡
    # scheduler.start()
    app.run(host='0.0.0.0', port=5001, debug=True)
else:
    # if __name__ == "__main__":
    # $ export FLASK_APP=/home/server.py
    # $ flask run --host=0.0.0.0 >null 2>&1 &
    #     app.config['JSON_AS_ASCII'] = False
    # print("启动https服务")
    # addtask()
    scheduler = BackgroundScheduler()
    scheduler.add_job(clear, 'cron', day_of_week='0-6',
                    hour=0, minute=0, second=0)  # 定时更新最近关卡
    scheduler.add_job(task_recent, 'interval', minutes=60)  # 定时更新最近关卡
    # scheduler.add_job(updatezhs, 'interval', hours=2) #定时更新zhs
    scheduler.add_job(addtask, 'interval', minutes=1) #补漏
    # scheduler.add_job(task_test, 'interval', seconds=10)
    scheduler.start()

    # app.run(host='0.0.0.0', port='443', debug=False, ssl_context='adhoc')
    app.run(host='0.0.0.0', port=5001, debug=True)
    # try:
    #     # 模拟主进程持续运行
    #     while True:
    #         time.sleep(20)
    #         # print('sleep')
    # except(KeyboardInterrupt, SystemExit):
    #     # Not strictly necessary if daemonic mode is enabled but should be done if possible
    #     scheduler.shutdown()
    #     print('Exit The Job!')