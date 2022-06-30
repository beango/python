#!/usr/bin/python
# -*- coding:utf-8 -*-

import urllib
import urllib2
import time
import os
import sys
import json
import logging
import logging.config
import ConfigParser
import optparse
import re
import traceback
import random

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
RED = "\x1B[31m"
GREEN = "\x1B[32m"
RESET = "\x1B[0m"
MAGENTA = "\x1B[35m"
HIDE_CURSOR = "\x1b[?25l"
SHOW_CURSOR = "\x1b[?25h"

def get(url, data):
    var_list = []
    for k in data.keys():
        var_list.append(k + "=" + str(data[k]))
    url += "?" + "&".join(var_list)
    
    request = urllib2.Request(url)
    request.add_header('User-Agent', random.choice(my_headers))
    response = urllib2.urlopen(request)
    # response.add_header('User-Agent', random.choice(my_headers))
    # print response.read()
    return response.read()

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
    if stock_id not in OUTLAND_STOCK:
        request = urllib2.Request(stock_api_url.format(stock_id))
        request.add_header("Referer", "http://finance.sina.com.cn")
        response = urllib2.urlopen(request)
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
    desc_dict = {
        "name" : u"基金名称".encode('gb18030'),
        "dwjz" : u"单位价值".encode('gb18030'),
        "gz" : u"估值".encode('gb18030'),
        "gszzl" : u"估算涨幅".encode('gb18030'),
        "gssy" : u"估算收益".encode('gb18030'),
        "gszz" : u"昨日总值".encode('gb18030'),
        "gztime" : u"更新时间".encode('gb18030'),
        "total" : u"总值".encode("gb18030")
    }

    fund_dict_list.append(desc_dict)

    for fund_data in fund_data_list:
        fund_data = json.loads(fund_data)

        fund_dict = {}
        fund_dict["name"] = fund_data["Expansion"]["SHORTNAME"].encode('gb18030')
        fund_dict["gz"] = fund_data["Expansion"]["GZ"].encode('gb18030')
        fund_dict["dwjz"] = fund_data["Expansion"]["DWJZ"].encode('gb18030')
        if float(fund_data["Expansion"]["GSZZL"]) > 0:
           fund_data["Expansion"]["GSZZL"] = "+" + fund_data["Expansion"]["GSZZL"]  
        fund_dict["gszzl"] = fund_data["Expansion"]["GSZZL"].encode('gb18030')
        fund_dict["gztime"] = fund_data["Expansion"]["GZTIME"].encode('gb18030')
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
    name_max_len = max([len(f["name"]) for f in fund_dict_list])
    gz_max_len = max([len(f["gz"]) for f in fund_dict_list])
    dwjz_max_len = max([len(f["dwjz"]) for f in fund_dict_list])
    gszzl_max_len = max([len(f["gszzl"]) for f in fund_dict_list])
    gztime_max_len = max([len(f["gztime"]) for f in fund_dict_list])
    total_max_len = max([len(f["total"]) for f in fund_dict_list])
    gssy_max_len = max([len(f["gssy"]) for f in fund_dict_list])
    gszz_max_len = max([len(f["gszz"]) for f in fund_dict_list])

    print("_" * (name_max_len + gz_max_len + dwjz_max_len + gszzl_max_len + gztime_max_len + total_max_len + gssy_max_len + gszz_max_len + 23))

    total_value = 0
    sy_total_value = 0
    yesterday_total_value = 0
    for fund_dict in fund_dict_list:
        line = b"|" + fund_dict["name"].ljust(name_max_len) + \
        b" | " + fund_dict["dwjz"].ljust(dwjz_max_len) + \
        b" | " + fund_dict["gz"].ljust(gz_max_len) + b" | "

        if fund_dict["gszzl"].decode('gb18030') != u"估算涨幅":
            if float(fund_dict["gszzl"]) > 0:
                line += RED + fund_dict["gszzl"].ljust(gszzl_max_len) + RESET
            elif float(fund_dict["gszzl"]) < 0:
                print(type(fund_dict["gszzl"]), type(fund_dict["gszzl"].ljust(gszzl_max_len)))
                line += GREEN + fund_dict["gszzl"].ljust(gszzl_max_len) + RESET
            else:
                line += fund_dict["gszzl"].ljust(gszzl_max_len)
        else:
            line += fund_dict["gszzl"].ljust(gszzl_max_len)

        line += b" | " + fund_dict["gssy"].ljust(gssy_max_len)

        line += b" | " + fund_dict["gszz"].ljust(gssy_max_len)

        line += b" | " + fund_dict["total"].ljust(total_max_len)

        line += b" | " + fund_dict["gztime"].ljust(gztime_max_len) + b" | "

        print(line.decode('gb18030'))

        if fund_dict["total"].decode('gb18030') != u"总值":
            total_value += float(fund_dict['total'])

        if fund_dict["gszz"].decode('gb18030') != u"昨日总值":
            yesterday_total_value += float(fund_dict['gszz'])

        if fund_dict["gssy"].decode('gb18030') != u"估算收益":
            sy_total_value += float(fund_dict['gssy'])

    print
    print("今日基金收益: {0:.2f}".format(sy_total_value))
    print("昨日基金总值: {0:.2f}".format(yesterday_total_value))
    print("今日基金总值: {0:.2f}".format(total_value))

def get_all_stock_data(stock_id_list):
    stock_data_list = []
    for stock_id in stock_id_list:
        stock_data_list.append(get_stock(stock_id).decode("gbk"))
    return stock_data_list

def process_all_stock_data(stock_data_list):
    stock_dict_list = []
    desc_dict = {
        "name" : u"指数名称".encode('gb18030'),
        "index" : u"指数".encode('gb18030'),
        "change" : u"涨跌额".encode('gb18030'),
        "rate" : u"涨跌幅".encode('gb18030')
    }
    stock_dict_list.append(desc_dict)

    for stock_data in stock_data_list:
        stock_list = re.search(r"=\"([ \S]*)\"", stock_data).group(1).split(",")

        stock_dict = {}
        stock_dict["name"] = stock_list[0].encode('gb18030')
        stock_dict["index"] = stock_list[1].encode('gb18030')
        stock_dict["change"] = stock_list[2].encode('gb18030')

        stock_list[3] = stock_list[3]#.replace("%", "")
        if float(stock_list[3]) > 0:
            stock_list[3] = "+" + stock_list[3]
        stock_dict["rate"] = stock_list[3].encode('gb18030')
        stock_dict_list.append(stock_dict)
    return stock_dict_list

def print_all_stock_data(stock_dict_list):
    name_max_len = max([len(f["name"]) for f in stock_dict_list])
    index_max_len = max([len(f["index"]) for f in stock_dict_list])
    change_max_len = max([len(f["change"]) for f in stock_dict_list])
    rate_max_len = max([len(f["rate"]) for f in stock_dict_list])

    print("_" * (name_max_len + index_max_len + change_max_len + rate_max_len + 10))

    for stock_dict in stock_dict_list:
        line = b"|" + stock_dict["name"].ljust(name_max_len) + \
        b" | " + stock_dict["index"].ljust(index_max_len) + \
        b" | " + stock_dict["change"].ljust(change_max_len) + b" | "

        if stock_dict["rate"].decode('gb18030') != u"涨跌幅":
            if float(stock_dict["rate"]) > 0:
                line += RED + stock_dict["rate"].ljust(rate_max_len) + RESET
            elif float(stock_dict["rate"]) < 0:
                line += GREEN + stock_dict["rate"].ljust(rate_max_len) + RESET
            else:
                line += stock_dict["rate"].ljust(rate_max_len)
        else:
            line += stock_dict["rate"].ljust(rate_max_len)
        line += b"|"

        print(line.decode('gb18030'))

def main():
    parser = optparse.OptionParser()
    parser.add_option("-d", "--delay", dest="delay", default=6)
    (options, args) = parser.parse_args()

    cf = ConfigParser.ConfigParser()
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

            print CLEAR_SCREEN,
            print(MAGENTA + time.strftime("%Y-%m-%d %H:%M:%S").center(int(columns)) + RESET)
            print_all_stock_data(stock_dict_list)

            last_tick_time = now
        time.sleep(1)

def fund():
    parser = optparse.OptionParser()
    parser.add_option("-d", "--delay", dest="delay", default=6)
    (options, args) = parser.parse_args()

    cf = ConfigParser.ConfigParser()
    cf.read("./fund.conf")
    fund_id_list = cf.options("fund")
    stock_id_list = cf.options("stock")
    buy_fund_pair_list = cf.items("buy_fund")

    print(HIDE_CURSOR)
    
    fund_data_list = get_all_fund_data(fund_id_list)
    fund_dict_list = process_all_fund_data(fund_data_list, buy_fund_pair_list)

    rows, columns = os.popen('stty size', 'r').read().split()

    print(CLEAR_SCREEN)
    print(MAGENTA + time.strftime("%Y-%m-%d %H:%M:%S").center(int(columns)) + RESET)
    print
    print_all_fund_data(fund_dict_list)

    

if __name__ == "__main__":
    while 1:
        main()
    # fund()

# sshpass -p '9HLx63RwWMAe' scp -r ./fund.py root@106.75.148.48:/root
# sshpass -p '10HLx63RwWMAe' scp -P 26807 -r CC签到.py root@144.168.63.235:/root