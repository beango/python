#!/usr/bin/python
# -*- coding:utf-8 -*-

import urllib.request
import time
import os
import sys
import json
import logging
import logging.config
import configparser
import optparse
import re
import traceback
import random
from prettytable import PrettyTable
from colorama import Fore, Back, Style

ISTER = True

# 收集到的常用Header
my_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
]

# API_URL
fund_api_url = "https://fundmobapi.eastmoney.com/FundMApi/FundVarietieValuationDetail.ashx"
stock_api_url = "http://hq.sinajs.cn/list=s_{0}"
stock_outland_api_url = "http://hq.sinajs.cn/list={0}"

# 境外指数
OUTLAND_STOCK = ["int_nasdaq", "int_dji", "int_sp500", "int_hangseng"]

# 控制字符
CLEAR_SCREEN = "\x1B[2J\x1B[3J\x1B[H"
RED = Fore.RED
GREEN = Fore.GREEN
RESET = Style.RESET_ALL
MAGENTA = ""
HIDE_CURSOR = ""
SHOW_CURSOR = ""
CHAR_CODE="utf-8"

if not ISTER:
    RED=""
    GREEN=""
    RESET=""
    print("""<style type=\"text/css\">
    table {border-collapse: collapse;border-spacing: 0;}
    td,th {padding: 0;}
    .pure-table {border-collapse: collapse;border-spacing: 0;empty-cells: show;}
    .pure-table td,.pure-table th {font-size: inherit;margin: 0;overflow: visible;padding: .2em;}
    .pure-table thead {background-color: #e0e0e0;color: #000;text-align: left;vertical-align: bottom;}
    .pure-table td {background-color: transparent;}
    .pure-table-bordered tr:nth-child(even){background: #F5FAFA;}
    .scroll {display: flex;}
    .item {text-align: center;flex-shrink: 0;line-height: 50px;}
    </style>""")

def get(url, data):
    var_list = []
    for k in data.keys():
        var_list.append(k + "=" + str(data[k]))
    url += "?" + "&".join(var_list)

    headers = {
        'User-Agent': random.choice(my_headers)
    }
    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request)
    return response.read().decode('utf-8')

def get_fund(fund_id):
    data = {
        "FCODE" : fund_id,
        "deviceid" : "wap",
        "plat" : "Wap",
        "product" : "EFund",
        "version" : "2.0.0"
    }
    fund_str = get(fund_api_url, data)
    return fund_str

def get_stock(stock_id):
    response = None
    headers = {
        'User-Agent': random.choice(my_headers),
        "Referer": "http://finance.sina.com.cn"
    }
    if stock_id not in OUTLAND_STOCK:
        
        request = urllib.request.Request(url=stock_api_url.format(stock_id), headers=headers)
        response = urllib.request.urlopen(request)
        # return response.read().decode('utf-8')

        # request = urllib2.Request(stock_api_url.format(stock_id))
        # request.add_header("Referer", "http://finance.sina.com.cn")
        # response = urllib2.urlopen(request)
    else:
        request = urllib2.Request(stock_api_url.format(stock_id))
        request.add_header("Referer", "http://finance.sina.com.cn")
        response = urllib2.urlopen(request)
    return response.read()

def get_all_fund_data(fund_list):
    fund_data_list = []
    for fund_id in fund_list:
        fund_data_list.append(get_fund(fund_id))
    return fund_data_list

def process_all_fund_data(fund_data_list, buy_fund_pair_list):
    fund_dict_list = []
    for fund_data in fund_data_list:
        fund_data = json.loads(fund_data)

        fund_dict = {}
        fund_dict["name"] = fund_data["Expansion"]["SHORTNAME"]
        fund_dict["gz"] = fund_data["Expansion"]["GZ"]
        fund_dict["dwjz"] = fund_data["Expansion"]["DWJZ"]
        if float(fund_data["Expansion"]["GSZZL"]) > 0:
           fund_data["Expansion"]["GSZZL"] = "+" + fund_data["Expansion"]["GSZZL"]
        fund_dict["gszzl"] = fund_data["Expansion"]["GSZZL"]
        fund_dict["gztime"] = fund_data["Expansion"]["GZTIME"]
        fund_dict["total"] = 0
        fund_dict["gssy"] = 0
        fund_dict["gszz"] = 0
        for item in buy_fund_pair_list:
            if item[0] == fund_data["Expansion"]["FCODE"]:
                fund_dict["total"] = float(item[1]) * float(fund_dict["gz"])
                fund_dict["gszz"] = float(item[1]) * float(fund_dict["dwjz"])
                fund_dict["gssy"] = float(item[1]) * (float(fund_dict["gz"]) - float(fund_dict["dwjz"]))
                break

        fund_dict["total"] = "{0:.2f}".format(fund_dict["total"])
        fund_dict["gssy"] = "{0:.2f}".format(fund_dict["gssy"])
        fund_dict["gszz"] = "{0:.2f}".format(fund_dict["gszz"])

        fund_dict_list.append(fund_dict)
    return fund_dict_list

def print_all_fund_data(fund_dict_list):
    total_value = 0
    sy_total_value = 0
    yesterday_total_value = 0

    tb = PrettyTable()
    # tb.header = False
    tb.field_names = ["基金名称", "估值", "估算收益", "今日总值", "估值时间"]
    fund_str = "<div class=\"scroll\"><div class=\"item\"><table border=\"1\" class=\"pure-table pure-table-bordered\">"
    fund_str += "<tr><thead><th>名称</th><th>估算收益</th><th>总值</th></thead></tr>"
    for fund_dict in fund_dict_list:
        gszzl = fund_dict["gszzl"]
        fund_str += "<tr><td>"+fund_dict["name"]+"</br><font size=\"2.2\" color=\"#999\">" + fund_dict["gztime"] +"</font></td>"
        fund_str += "<td>" + fund_dict["gssy"]
        if fund_dict["gszzl"] != u"估算涨幅":
            if float(gszzl) > 0:
                fund_str += "</br><font color=red size=\"2.2\">" + gszzl + "%</font>"
            elif float(fund_dict["gszzl"]) < 0:
                fund_str += "</br><font color=green size=\"2.2\">" + gszzl + "%</font>"
        fund_str += "</td>"
        fund_str += "<td>" + fund_dict["total"] + "</td></tr>"
        
        if fund_dict["gszzl"] != u"估算涨幅":
            if float(gszzl) > 0:
                gszzl = RED + gszzl + RESET
            elif float(fund_dict["gszzl"]) < 0:
                gszzl = GREEN + gszzl + RESET

        tb.add_row([fund_dict["name"], fund_dict["gz"], fund_dict["gssy"]+"("+ gszzl+")", fund_dict["total"], fund_dict["gztime"]])
        
        if fund_dict["total"] != u"总值": 
            total_value += float(fund_dict['total'])

        if fund_dict["gszz"] != u"昨日总值":
            yesterday_total_value += float(fund_dict['gszz'])

        if fund_dict["gssy"] != u"估算收益":
            sy_total_value += float(fund_dict['gssy'])
    if not ISTER: print(fund_str + "</table></div></div>")

    # tb.max_width = 8
    # tb.align = 'l'
    syrate_total_value = sy_total_value / yesterday_total_value
    if ISTER:
        print(tb)
        if sy_total_value > 0 :
            print("今日基金收益: "+RED + "{0:.2f} ({1:.2%})".format(sy_total_value, syrate_total_value)+ RESET+"")
        elif sy_total_value < 0 :
            print("今日基金收益: "+GREEN + "{0:.2f} ({1:.2%})".format(sy_total_value, syrate_total_value)+ RESET+"")
        else:
            print("今日基金收益: {0:.2f} ({1:.2%})".format(sy_total_value, syrate_total_value))
        print("昨日基金总值: {0:.2f}".format(yesterday_total_value))
        print("今日基金总值: {0:.2f}".format(total_value))
    else:
        # print(tb.get_html_string(attributes={"id":"my_table", "class":"pure-table pure-table-bordered"}))
        if sy_total_value > 0 :
            print("今日基金收益: <font color=red>" + "{0:.2f}</font> (<font color=red>{1:.2%}</font>)".format(sy_total_value, syrate_total_value))
        elif sy_total_value < 0 :
            print("今日基金收益: <font color=green>" + "{0:.2f}</font> (<font color=green>{1:.2%}</font>)".format(sy_total_value, syrate_total_value))
        else:
            print("今日基金收益: {0:.2f} ({1:.2%})".format(sy_total_value, syrate_total_value))
        print("</br>昨日基金总值: {0:.2f}".format(yesterday_total_value))
        print("</br>今日基金总值: {0:.2f}".format(total_value))

def get_all_stock_data(stock_id_list):
    stock_data_list = []
    for stock_id in stock_id_list:
        stock_data_list.append(get_stock(stock_id).decode("gbk"))
    return stock_data_list

def process_all_stock_data(stock_data_list):
    stock_dict_list = []
    desc_dict = {
        "name" : u"指数名称",
        "index" : u"指数",
        "change" : u"涨跌额",
        "rate" : u"涨跌幅"
    }
    # stock_dict_list.append(desc_dict)

    for stock_data in stock_data_list:
        stock_list = re.search(r"=\"([ \S]*)\"", stock_data).group(1).split(",")

        stock_dict = {}
        stock_dict["name"] = stock_list[0]
        stock_dict["index"] = stock_list[1]
        stock_dict["change"] = stock_list[2]

        stock_list[3] = stock_list[3]#.replace("%", "")
        if float(stock_list[3]) > 0:
            stock_list[3] = "+" + stock_list[3]
        stock_dict["rate"] = stock_list[3]
        stock_dict_list.append(stock_dict)
    return stock_dict_list

def print_all_stock_data(stock_dict_list):
    tb = PrettyTable()
    tb.field_names = ["指数名称", "指数", "涨跌额", "涨跌幅"]
    for stock_dict in stock_dict_list:
        rate = stock_dict["rate"]
        if stock_dict["rate"] != u"涨跌幅":
            if float(rate) > 0:
                rate = RED + rate + RESET
            elif float(stock_dict["rate"]) < 0:
                rate = GREEN + rate + RESET
        tb.add_row([stock_dict["name"], stock_dict["index"], stock_dict["change"], rate])
    print(tb)
        
def main():
    parser = optparse.OptionParser()
    parser.add_option("-d", "--delay", dest="delay", default=6)
    (options, args) = parser.parse_args()

    cf = configparser.ConfigParser()
    cf.read("./fund.conf")
    fund_id_list = cf.options("fund")
    stock_id_list = cf.options("stock")
    buy_fund_pair_list = cf.items("buy_fund")

    print(HIDE_CURSOR)
    last_tick_time = 0

    while 1:
        now = time.time()
        if now > last_tick_time + int(options.delay):
            stock_data_list = get_all_stock_data(stock_id_list)
            stock_dict_list = process_all_stock_data(stock_data_list)

            rows, columns = os.popen('stty size', 'r').read().split()
            print(CLEAR_SCREEN)
            print(MAGENTA + time.strftime("%Y-%m-%d %H:%M:%S").center(int(columns)) + RESET)
            print_all_stock_data(stock_dict_list)

            last_tick_time = now
        time.sleep(1)

def fund():
    parser = optparse.OptionParser()
    parser.add_option("-d", "--delay", dest="delay", default=6)
    (options, args) = parser.parse_args()

    cf = configparser.ConfigParser()
    cf.read("./fund.conf")
    fund_id_list = cf.options("fund")
    stock_id_list = cf.options("stock")
    buy_fund_pair_list = cf.items("buy_fund")

    if ISTER:
        print(HIDE_CURSOR)

    fund_data_list = get_all_fund_data(fund_id_list)
    fund_dict_list = process_all_fund_data(fund_data_list, buy_fund_pair_list)

    if ISTER:
        print(CLEAR_SCREEN)
    print(time.strftime("%Y-%m-%d %H:%M:%S"))
    print
    print_all_fund_data(fund_dict_list)



if __name__ == "__main__":
    # if ISTER:
    #     main()
    ISTER = True
    if len(sys.argv) > 1 and sys.argv[1] == "1": ISTER = False
    fund()


# sshpass -p '9HLx63RwWMAe' scp -r ./fund.py root@106.75.148.48:/root
# sshpass -p '10HLx63RwWMAe' scp -P 26807 -r CC签到.py root@144.168.63.235:/root
