# -*- coding:UTF-8 -*-
from urllib import request
import bs4
from bs4 import BeautifulSoup
import json
import time
import os
import socket
import urllib
import re
import sys
import html
import base64
from urllib.request import quote
import logging
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed  # 线程池，进程池
import threading
from operator import itemgetter  # itemgetter用来去dict中的key，省去了使用lambda函数
from itertools import groupby  # itertool还包含有其他很多函数，比如将多个list联合起来。。
import datetime
import difflib
import execjs
import filterdict

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
isLocale = ip == "127.0.0.1"
print(hostname, ip, isLocale)

checkexists = True
timeout = 8
socket.setdefaulttimeout(timeout)
head = {}
head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
httpproxy_handler = request.ProxyHandler({"socks5": "127.0.0.1:7891"})
nullproxy_handler = request.ProxyHandler({})
opener = request.build_opener(nullproxy_handler)
allzhs = {}


re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
re_script = re.compile(
    '<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
re_br = re.compile('<br\s*?/?>')  # 处理换行
re_h = re.compile('</?\w+[^>]*>')  # HTML标签
re_comment = re.compile('<!--[^>]*-->')  # HTML注释

if os.path.exists('static/allzhs.json'):
    with open('static/allzhs.json', 'r') as json_file:
        if json_file != '':
            allzhs = json.load(json_file)


def not_empty(s):
    return s and s.strip()


def compare2file(file1, file2):
    if not os.path.exists(file1) or not os.path.exists(file2):
        return False
    f1 = open(file1, 'r')
    t1 = f1.read()
    f1.close()
    f2 = open(file2, 'r')
    t2 = f2.read()
    f2.close()
    s = difflib.SequenceMatcher(None, t1, t2)
    return s.ratio() == 1.0
# 擊倒 {{1522|40}} 1 次——開放關卡[[世界初探]] 替换为
# 擊倒 ![1522](zhs/1522i.png) 1 次——開放關卡[[世界初探]]
# {{C169|30}}[[影之鐵壁龍符]] 1粒    ==>  ![影之鐵壁龍符](lk/C169.png)


def replace1(d):
    d = re.sub(r'{{([\d]+)[\|]([^}]{0,})}}', r'![\1](zhs/\1i.png)', d)
    d = re.sub(r'{{(C[\d]+)[\|]([^}]{0,})}}\s*(\[\[([^\]]+?)\]\])*',
               r'![\1\4](lk/\1.png)[\1\4](/pages/index/lk/lk?id=\1)', d)
    # d=re.sub(r'\[\[([^\]]*)\]\]',r'[\1](/pages/index/detail/detail?name2=\1)', d)
    d = re.split(r'\[\[([^\]]*)\]\]', d)
    for i in range(1, len(d), 2):
        _t = d[i]
        if _t == "行商要塞":
            d[i] = "[" + _t + "]()"
        else:
            _ar = _t.split("|")
            if len(_ar) == 2:
                d[i] = "[" + _ar[1] + \
                    "](/pages/index/detail/detail?name2=" + \
                       quote(_ar[0].split('#')[0])+")"
            if len(_ar) == 1:
                d[i] = "[" + _ar[0] + \
                    "](/pages/index/detail/detail?name2="+quote(_ar[0])+")"
    return "".join(d)
# {{1522|40}} -->  {{1522*40}}


def replacecommon(title):
    title = re.sub(
        r'({{魔法石}})', r'![魔法石](toswikiapic/Gift-魔法石.png)', title)
    title = re.sub(
        r'({{布蘭克之匙}})', r'![布蘭克之匙](toswikiapic/yaoshi.png)', title)
    title = re.sub(
        r'({{金幣}})', r'![金幣](toswikiapic/金幣.png)', title)
    title = re.sub(
        r'({{Gift[\|]體力回復劑[\|].*}})', r'![體力回復劑](toswikiapic/Gift-體力回復劑.png)', title)
    title = re.sub(
        r'({{Gift[\|]體力[\|].*}})', r'![體力](toswikiapic/體力.png)', title)
    title = re.sub(
        r'({{Gift[\|]魔法石[\|].*}})', r'![魔法石](toswikiapic/Gift-魔法石.png)', title)
    title = re.sub(
        r'({{Gift[\|]戰靈回復劑[\|].*}})', r'![戰靈回復劑](toswikiapic/Gift-戰靈回復劑.png)', title)
    title = re.sub(
        r'({{Gift[\|]戰靈藥水[\|].*}})', r'![戰靈藥水](toswikiapic/戰靈藥水.png)', title)
    title = re.sub(r'{{([\d]+)\|{1}([^}]*)}}',
                   r'![\1](zhs/\1i.png)', title)
    title = re.sub(r'\[\[([^\]]*)\]\]',
                   r'[\1](/pages/index/detail/detail?name2=\1)', title)
    return title


def replace2(d):
    d = re.split(r'{{([^}]*)}}', d)
    for i in range(1, len(d), 2):
        d[i] = "{{" + d[i].replace("|", "*") + "}}"
    return "".join(d)


def downimg(datasrc, savesrc):
    if datasrc != None and datasrc != 'None' and not os.path.exists(savesrc):
        i = 3
        while i > 0:
            try:
                request.urlretrieve(datasrc, savesrc)
                i = 0
                return True
            except:
                print("downimg::下载失败，重试一次！", datasrc)
                i = i-1
        return False
    return True


def getrecentimg():
    # download_url = "https://tos.fandom.com/zh/wiki/%E7%A5%9E%E9%AD%94%E4%B9%8B%E5%A1%94_%E7%B9%81%E4%B8%AD%E7%B6%AD%E5%9F%BA"
    download_url = "https://tos.fandom.com/zh/wiki/Template:CurrentEvents?a=1"
    soup = downlink(download_url)
    if soup == None:
        return
    textarea = soup.findAll('div', class_='mw-parser-output')[0]
    for img in textarea.findAll('img'):
        name = img.get('data-image-name')
        url = img.get('data-src')
        if url == None:
            url = img.get('src')
        downimg(url, 'static/toswikiapic/' + name)
    f = open('static/daily2.json', encoding='utf-8')
    res = f.read()
    params_json = json.loads(res)
    for section in params_json:
        for fb in section["data"]:
            if "orgtitle" in fb:
                getfbimg2(fb["orgtitle"])
            else:
                getfbimg2(fb["title"])
    f.close()


def getfbimg2(fbname):
    print(fbname)
    download_url = "https://tos.fandom.com/zh/wiki/"+quote(fbname)
    soup = downlink(download_url)
    # f =open('1.html', encoding='utf-8')
    # download_html=f.read()
    # soup = BeautifulSoup(download_html, 'lxml')
    if soup == None:
        return
    textarea = soup.findAll('div', class_='mw-parser-output')[0]
    for img in textarea.findAll('img'):
        name = img.get('data-image-name')
        url = img.get('data-src')
        if url == None:
            url = img.get('src')
        downimg(url, 'static/zhs/' + name)


def getfbimg(fbname):
    print(fbname)
    download_url = "https://tos.fandom.com/zh/wiki/"+quote(fbname)
    soup = downlink(download_url)
    # f =open('1.html', encoding='utf-8')
    # download_html=f.read()
    # soup = BeautifulSoup(download_html, 'lxml')
    if soup == None:
        return
    textarea = soup.findAll('div', class_='mw-parser-output')[0]
    for img in textarea.findAll('img'):
        name = img.get('data-image-name')
        url = img.get('data-src')
        if url == None:
            url = img.get('src')
        downimg(url, 'static/fbimg/' + name)


def getmainlineimg(name):
    download_url = "https://tos.fandom.com/zh/wiki/Template:" + name
    soup = downlink(download_url)
    if soup == None:
        return
    textarea = soup.findAll('div', class_='mw-parser-output')[0]
    for img in textarea.findAll('img'):
        name = img.get('data-image-name')
        url = img.get('data-src')
        if url == None:
            url = img.get('src')
        downimg(url, 'static/fbimg/' + name)
        downimg(url, 'static/zhs/' + name)


def getrecent():
    download_url = "https://tos.fandom.com/zh/wiki/Template:CurrentEvents?action=edit"
    soup = downlink(download_url)
    if soup == None:
        return
    textarea = soup.findAll('textarea')[0].string
    textarea = re_comment.sub('', textarea)
    # f =open('1.html', encoding='utf-8')
    # textarea=f.read()
    textarea = re_comment.sub('', textarea)
    eventSections = re.split('{{EventSection\|', textarea)
    d = []
    events = []
    nowtime = datetime.datetime.now()
    for section in eventSections:
        if str.strip(section) == '':
            continue
        sectionline = section.splitlines()
        sectiontitle = ''
        section = []
        for lineidx in range(0, len(sectionline)):
            line = sectionline[lineidx]
            start = ''
            end = ''
            if lineidx == 0:
                sectiontitle = line.replace("}}", "")
            if re.match('^{{Event\|{{DIcon\|([-]{0,1}\d+)\|(.*)}}(.*)$', line):
                if (sectionline[lineidx+1][0] == '|'):
                    start = str.strip(
                        sectionline[lineidx+1][1:].split('|')[0]).replace("}}", "")
                    end = str.strip(
                        sectionline[lineidx+1][1:].split('|')[1].replace("}}", "").replace("-->", ""))
                s2 = re.split(
                    '^{{Event\|{{DIcon\|([-]{0,1}\d+)\|(.*)}}(.*)$', line)
                if len(s2) > 4:
                    id = str.strip(s2[1])
                    title = str.strip(s2[2])
                    type = str.strip(s2[3])
                    if type == '':
                        type = 'Event'
                    if id[0] == '-':
                        img_src = 'toswikiapic/S'+id+'i.png'
                    else:
                        img_src = 'toswikiapic/'+id+'i.png'
                if len(s2) == 1:
                    id = ""
                    type = ""
                    img_src = ''
                    if s2[0].index('{{Event|') == 0:
                        title = s2[0].replace('{{Event|', '')
                    else:
                        title = s2[0]
                endstr = str.strip(end)
                if(endstr != ''):
                    if endstr.find(" ") > -1:
                        endtime = datetime.datetime.strptime(
                            endstr, "%Y/%m/%d %H:%M")
                    else:
                        endtime = datetime.datetime.strptime(
                            endstr, "%Y/%m/%d")+datetime.timedelta(days=1)
                    if endtime > nowtime:
                        section.append({
                            'orgtitle': title,
                            'title': title.replace("/", "*"),
                            'type': type,
                            'img': img_src,
                            'start': start,
                            'end': endstr
                        })
                else:
                    section.append({
                        'orgtitle': title,
                        'title': title.replace("/", "*"),
                        'type': type,
                        'img': img_src,
                        'start': start,
                        'end': endstr
                    })
            elif re.match('^{{Event\|{{Gift\|(.*)}}$', line):
                if (sectionline[lineidx+1][0] == '|'):
                    start = str.strip(sectionline[lineidx+1][1:].split('|')[0])
                    end = str.strip(
                        sectionline[lineidx+1][1:].split('|')[1].replace("}}", "").replace("-->", ""))
                title = re.split('^{{Event\|{{Gift\|(.*)}}$', line)[1]
                title = title.replace('gift=', '').split('|')
                if(end.find(" ") > -1):
                    endtime = datetime.datetime.strptime(end, "%Y/%m/%d %H:%M")
                else:
                    endtime = datetime.datetime.strptime(
                        end, "%Y/%m/%d")+datetime.timedelta(days=1)
                if endtime > nowtime:
                    extgift = ""
                    if len(title) > 2:
                        extgift = " 共 " + title[2] + "次"
                    if title[0].find("seal=") == 0:
                        title[0] = "!["+title[0].replace(
                            "seal=", "")+"](toswikiapic/Gift-抽卡機會.png)"+" ["+title[0].replace("seal=", "")+"]()"
                    if title[0] == "限時體力回復劑":
                        title[0] = "![限時體力回復劑](toswikiapic/Gift-體力回復劑.png)"
                        extgift = '(活动时限内领取)'
                    section.append({'title': title[0] + "*" + title[1] + extgift,
                                    'type': '',
                                    'img': '',
                                    'orginimg': '',
                                    'start': start,
                                    'end': end
                                    })
            elif re.match('^{{Event\|(.*)$', line):
                if (sectionline[lineidx+1][0] == '|'):
                    _a = sectionline[lineidx+1][1:].split('|')
                    start = str.strip(_a[0]).replace(
                        "}}", "")
                    if(len(_a) == 2):
                        end = str.strip(_a[1].replace(
                            "}}", "").replace("-->", ""))
                    else:
                        end = start
                title = re.split('^{{Event\|(.*)$', line)[1]
                if(end.find(" ") > -1):
                    endtime = datetime.datetime.strptime(end, "%Y/%m/%d %H:%M")
                else:
                    if end != '':
                        endtime = datetime.datetime.strptime(
                            end, "%Y/%m/%d")+datetime.timedelta(days=1)
                if endtime > nowtime:
                    title = replacecommon(title)
                    title = replace1(title)
                    section.append({
                        'line': line,
                        'orgtitle': title,
                        'title': title.replace("/", "*"),
                        'type': '',
                        'img': '',
                        'orginimg': '',
                        'start': start,
                        'end': end
                    })
        for t in sectiontitle.split("/"):
            if t[0:2] == "[[" and t[-2:] == "]]":
                sectiontitle2 = t.replace("[[", "").replace("]]", "")
                if sectiontitle2.split("|")[0] != '修羅場活動' \
                        and sectiontitle2.split("|")[0] != '魔神戰活動' \
                        and sectiontitle2.split("|")[0] != '公會討伐戰':
                    download_url = "https://tos.fandom.com/zh/wiki/" + \
                        quote(sectiontitle2)+"?action=edit"
                    soup = downlink(download_url)
                    if soup == None:
                        return
                    textarea = soup.findAll('textarea')
                    if textarea and len(textarea) > 0:
                        textarea = textarea[0].string
                    textarea = re.split(
                        r'<poem>([^<]*)<\s*/\s*poem\s*>', textarea)[1]
                    # f =open('1.html', encoding='utf-8')
                    # textarea=f.read()
                    events.append({"title": sectiontitle2, "detail": textarea})
        sectiontitle = sectiontitle.replace("[[", "").replace("]]", "")
        if len(sectiontitle.split("|")) == 2:
            sectiontitle = sectiontitle.split("|")[1]
        d.append({'name': sectiontitle, 'data': section})
    fw = open('static/daily1.json', 'w', encoding='utf-8')
    json.dump(d, fw, ensure_ascii=False, indent=2)
    fw.close()
    isdiff = compare2file("static/daily1.json", "static/daily2.json")
    f = open('static/ver.json', encoding='utf-8')
    v = json.loads(f.read())
    if 'recent' not in v or not isdiff:
        os.rename("static/daily1.json", "static/daily2.json")
        v['recent'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fw = open('static/ver.json', 'w', encoding='utf-8')
        json.dump(v, fw, ensure_ascii=False, indent=2)
        fw.close()
    f.close()
    fw = open('static/event.json', 'w', encoding='utf-8')
    json.dump(events, fw, ensure_ascii=False, indent=2)
    fw.close()

# 下载召唤兽图片


def getzhs(card):
    # if not os.path.exists("static/zhs/" + card + "i.png"):
    #     href = "https://tos.fandom.com/zh/wiki/Template:" + quote(card)
    #     soup = downlink(href)
    #     if soup == None: return
    #     daily=soup.findAll('div', class_='mw-parser-output')
    #     zshobj = daily[0].p.span.a.img
    #     zshname = zshobj.get("alt")
    #     img_src = 'static/zhs/' + zshname
    #     downimg(zshobj.get("src"), img_src)
    if not os.path.exists("static/zhs/" + card + ".json") or True:
        href = "https://tos.fandom.com/zh/wiki/Template:" + \
            quote(card) + "?action=edit"
        soup = downlink(href)
        if soup == None:
            return
        textarea = soup.findAll('textarea')[0].string
        d = {}
        for line in textarea.splitlines():
            _s = line.split('=')
            if len(_s) == 2:
                _name = str.strip(_s[0])[1:]
                d[_name] = str.strip(_s[1])
                if _name == 'skill' or _name == 'skill2' or _name == 'lskill':
                    d[_name] = str.strip(_s[1].replace("/", ""))
                    getskill(d[_name], _s[1])
        fw = open('static/zhs/'+card+'.json', 'w', encoding='utf-8')
        json.dump(d, fw, ensure_ascii=False, indent=2)


def getalllk():
    href = "https://tos.fandom.com/zh/wiki/" + \
        quote("龍刻圖鑒")+"?action=edit"  # 龍刻武裝圖鑒
    soup = downlink(href)
    if soup == None:
        return
    textarea = soup.findAll('textarea')[0].string
    lkgroup = re.split('{{龍刻圖鑒\|(.*)}}', textarea)
    lkarray = []
    for i in range(1, len(lkgroup), 2):
        for lk in lkgroup[i].split("|"):
            lk = str.strip(lk)
            if lk == "":
                continue
            if not os.path.exists('static/lk/'+lk+'.json'):
                getlk(lk)
            lkarray.append({"name": lk})

    href = "https://tos.fandom.com/zh/wiki/"+quote("龍刻武裝圖鑒")+"?action=edit"
    soup = downlink(href)
    if soup == None:
        return
    textarea = soup.findAll('textarea')[0].string
    # f =open('2.txt', encoding='utf-8')
    # textarea=f.read()
    lkgroup = re.split('{{龍刻圖鑒\|(.*)}}', textarea)
    lkarray = []
    for i in range(1, len(lkgroup), 2):
        for lk in lkgroup[i].split("|"):
            lk = str.strip(lk)
            if lk == "":
                continue
            if not os.path.exists('static/lk/'+lk+'.json'):
                getlk(lk)
            lkarray.append({"name": lk})
    fw = open('static/lk.json', 'w', encoding='utf-8')
    json.dump(lkarray, fw, ensure_ascii=False, indent=2)


def getalllkimg():
    download_url = "https://tos.fandom.com/zh/wiki/" + quote("龍刻圖鑒")
    soup = downlink(download_url)
    if soup == None:
        return
    textarea = soup.findAll('div', class_='mw-parser-output')[0]
    for img in textarea.findAll('img'):
        name = img.get('data-image-name')
        url = img.get('data-src')
        if url == None:
            url = img.get('src')
        if not os.path.exists('static/lk/' + name):
            downimg(url, 'static/lk/' + name)
    download_url = "https://tos.fandom.com/zh/wiki/" + quote("龍刻武裝圖鑒")
    soup = downlink(download_url)
    if soup == None:
        return
    textarea = soup.findAll('div', class_='mw-parser-output')[0]
    for img in textarea.findAll('img'):
        name = img.get('data-image-name')
        url = img.get('data-src')
        if url == None:
            url = img.get('src')
        if not os.path.exists('static/lk/' + name):
            downimg(url, 'static/lk/' + name)


def getlk(no):
    if not os.path.exists("static/lk/" + no + ".json"):
        href = "https://tos.fandom.com/zh/wiki/Template:"+no+"?action=edit"
        soup = downlink(href)
        if soup == None:
            return
        textarea = soup.findAll('textarea')[0].string
        # f =open('1.html', encoding='utf-8')
        # textarea=f.read()
        d = {}
        for line in textarea.splitlines():
            _s = line.split('=')
            if len(_s) == 2:
                _name = str.strip(_s[0])[1:]
                d[_name] = str.strip(_s[1])
                if _name == 'skill' or _name == 'lskill':
                    getskill(d[_name])
        fw = open('static/lk/'+no+'.json', 'w', encoding='utf-8')
        json.dump(d, fw, ensure_ascii=False, indent=2)


# 下载龙刻
def getlkimg(id):
    if checkexists and os.path.exists('static/lk/' + id + '.png'):
        return
    href = "https://tos.fandom.com/zh/wiki/Template:" + id
    soup = downlink(href)
    if soup == None:
        return
    daily = soup.findAll('div', class_='mw-parser-output')
    obj = daily[0].p.span.a.img
    name = obj.get("alt")
    img_src = 'static/lk/' + name
    downimg(obj.get("src"), img_src)

# 王关宝相掉落金币


def getchest():
    src = "https://static.wikia.nocookie.net/tos/images/f/f4/ICON075.png/revision/latest/scale-to-width-down/39?cb=20130924033809&path-prefix=zh"
    img_src = 'static/common/chest.png'
    downimg(src, img_src)


def getesimg(num):
    href = "https://tos.fandom.com/zh/wiki/%E6%95%B5%E4%BA%BA%E6%8A%80%E8%83%BD/"+num
    soup = downlink(href)
    if soup == None:
        return
    table = soup.findAll('table', class_='wikitable')[0]
    for img in table.findAll('img'):
        name = img.get('data-image-name')
        url = img.get('data-src')
        src = img.get('src')
        if url != None:
            downimg(url, 'static/es/' + name)
        if src != None:
            downimg(src, 'static/es/' + name)


def getskill(skillname, skillorgname):
    # if checkexists and os.path.exists('static/skill/'+skillname+'.json'):
    # return
    href = "https://tos.fandom.com/zh/wiki/Template:" + \
        quote(skillname)+"?action=edit"
    if skillorgname:
        href = "https://tos.fandom.com/zh/wiki/Template:" + \
            quote(skillorgname)+"?action=edit"
    soup = downlink(href)
    if soup == None:
        return
    daily = soup.findAll('textarea')[0].string
    id = ''
    name = ''
    effect = ''
    icon = ''
    content = ''
    d = {}
    for line in daily.splitlines():
        _s = re.split(r'^\|(.+?)=', line)
        if len(_s) == 3:
            _name = str.strip(_s[1])
            d[_name] = re.sub(r"\[board=(.*)\](.*)\[/board\]",
                              r'\2', str.strip(_s[2]))
    skillnamefile = skillname.replace("/", '')
    fw = open('static/skill/'+skillnamefile+'.json', 'w', encoding='utf-8')
    json.dump(d, fw, ensure_ascii=False, indent=2)

# 下载技能


def getes(num):
    esjson = 'static/es/' + num + '.json'
    if checkexists and os.path.exists(esjson):
        f = open(esjson, encoding='utf-8')
        res = f.read()
        return {"img": json.loads(res)["icon"], "title": json.loads(res)["title"]}
    href = "https://tos.fandom.com/zh/wiki/Template:ES"+num+"?action=edit"
    soup = downlink(href)
    if soup == None:
        return
    daily = soup.findAll('textarea')[0].string
    id = ''
    name = ''
    effect = ''
    icon = ''
    content = ''
    for line in daily.splitlines():
        if line.find('|id=') > -1:
            id = line[4:]
        if line.find('|name=') > -1:
            name = line[6:]
        if line.find('|effect=') > -1:
            effect = line[8:]
        if line.find('|content=') > -1:
            content = line[9:]
        if line.find('|icon') > -1:
            _icon = str.strip(line.split('=')[1])
            if not os.path.exists('static/es/' + _icon):
                getesimg(num)
        else:
            _icon = ""
        if _icon != '':
            icon += '|es/'+_icon
    if icon != '':
        icon = icon[1:]
    effect = html.unescape(effect)
    obj = {}
    obj["no"] = id
    name = name.replace("？", "")
    name = re_h.sub('', name)
    esimgname = name
    obj["title"] = name  # 技能通称
    obj["effect"] = effect  # 技能描述
    obj["content"] = content
    obj["icon"] = icon
    fw = open(esjson, 'w', encoding='utf-8')
    json.dump(obj, fw, ensure_ascii=False, indent=2)
    return {"img": icon, "title": obj["title"]}

# 下载故人技能


def getdres(num):
    esjson = 'static/es/' + num + '.json'
    if checkexists and os.path.exists(esjson):
        f = open(esjson, encoding='utf-8')
        res = f.read()
        return {"img": json.loads(res)["icon"], "title": json.loads(res)["title"]}
    href = "https://tos.fandom.com/zh/wiki/" + \
        quote("敵人技能") + "/" + num + "?action=edit"
    soup = downlink(href)
    if soup == None:
        return
    daily = soup.findAll('textarea')[0].string
    id = ''
    name = ''
    effect = ''
    icon = ''
    content = ''
    for line in daily.splitlines():
        if line.find('|id=') > -1:
            id = line[4:]
        if line.find('|name=') > -1:
            name = line[6:]
        if line.find('|effect=') > -1:
            effect = line[8:]
        if line.find('|content=') > -1:
            content = line[9:]
        if line.find('|icon') > -1:
            _icon = str.strip(line.split('=')[1])
            if not os.path.exists('static/es/' + _icon):
                getesimg(num)
        else:
            _icon = ""
        if _icon != '':
            icon += '|es/'+_icon
    if icon != '':
        icon = icon[1:]
    effect = html.unescape(effect)
    obj = {}
    obj["no"] = id
    esimgname = name
    obj["title"] = name  # 技能通称
    obj["effect"] = effect  # 技能描述
    obj["content"] = content
    obj["icon"] = icon
    fw = open(esjson, 'w', encoding='utf-8')
    json.dump(obj, fw, ensure_ascii=False, indent=2)
    return {"img": icon, "title": obj["title"]}


def downurl(href):
    i = 3
    while i > 0:
        try:
            download_req = request.Request(url=href, headers=head)
            download_response = opener.open(download_req)
            download_html = download_response.read().decode('utf-8', 'ignore')
            i = 0
            return download_html
        except Exception as e:
            print("downlink::下载失败，重试一次！", href, e)
            # logging.exception(e)
            i = i-1
    return None


def downlink(href):
    download_html = downurl(href)
    if download_html != None:
        return BeautifulSoup(download_html, 'lxml')
    return None


def getrecenttask():
    f = open('static/daily2.json', encoding='utf-8')
    res = f.read()
    params_json = json.loads(res)
    for section in params_json:
        for fb in section["data"]:
            gettask(fb)


def getmainlinetask():
    f = open('static/mainline.json', encoding='utf-8')
    res = f.read()
    params_json = json.loads(res)
    for section in params_json:
        for fb in section["data"]:
            for fb2 in fb["data"]:
                if not os.path.exists('static/stages/' + fb2["title"] + '.json'):
                    gettask(fb2)


def gettask_old(fb):
    if fb["type"] == '':
        return
    maintitle = fb["title"]
    href = "https://tos.fandom.com/zh/wiki/"+quote(fb["title"])+"?action=edit"
    if "orgtitle" in fb:
        href = "https://tos.fandom.com/zh/wiki/" + \
            quote(fb["orgtitle"])+"?action=edit"
    if fb["type"] == '旅人的記憶':
        href += '&veswitched=1'
    print('更新副本 ------> ', maintitle, fb["type"], href)
    soup = downlink(href)
    if soup == None:
        return
    ta = soup.findAll('textarea')
    if ta == None or len(ta) == 0:
        return
    daily = ta[0].string
    # f =open('1.html', encoding='utf-8')
    # daily=f.read()
    _timearr = re.split("==開放時間記錄==([\s\S]*?)==", daily)
    openhis = []
    if len(_timearr) == 3:  # 循环 開放時間記錄
        for d in _timearr[1].splitlines():
            if str.strip(d) == '':
                continue
            d = re.sub(r'{{([\d]+)\|([\d]+)}}', r'{{\1*\2}}', d)
            if(d.find("{{Event2|") == 0):
                _oarr = d.split('|')
                _start, _end, _note = '', '', ''
                if len(_oarr) > 1:
                    _note = _oarr[1]
                if len(_oarr) > 2:
                    _start = _oarr[2].replace("}}", "")
                if len(_oarr) > 3:
                    _end = _oarr[3].replace("}}", "")
                openhis.append({"start": str.strip(_start), "end": str.strip(
                    _end), "note": str.strip(_note), 'cj': [], 'cishujl': []})
    _timearrjl = re.split("==通關次數獎勵==([\s\S]*?)==", daily)  # 通關次數獎勵
    if len(_timearrjl) == 3:  # 循环 開放時間記錄
        timejl = re_h.sub('', _timearrjl[1])  # 去掉HTML 标签
        timejl = re_comment.sub('', timejl)  # 去掉HTML注释
        t = ""
        for d in timejl.splitlines():
            d = str.strip(d)
            if d == '':
                continue
            if(d.rfind(" 獎勵=") > -1):
                t = d.replace(" 獎勵=", "")
            d = d[2:-2]
            if(d.find("通關獎勵格") == 0):
                for _h in openhis:
                    if _h["start"].find(t) == 0:
                        d = re.sub(r'{{([^}]+)\|([^}]*)}}', r'{{\1*\2}}', d)
                        d = re.sub(r'{{C([^}]+)\*{1}([^}]*)}}',
                                   r'![C\1](lk/C\1.png)', d)
                        d = re.sub(r'{{([\d]+)\*{1}([^}]*)}}',
                                   r'![\1](zhs/\1i.png)', d)
                        jldarr = d.split('|')  # 奖励召唤兽 id
                        if(jldarr[1][0:2] == 'f='):
                            cishujl = {}
                            cishujl["cs_jltj"] = "首次通过 ["+jldarr[2]+"]()"
                            if(jldarr[5].find('other=') == 0):
                                cishujl["cs_jl"] = jldarr[5].split(
                                    "=")[1] + " * " + jldarr[6]
                            _h["cishujl"].append(cishujl)
                        if len(jldarr) > 3:
                            if jldarr[3] != '':
                                cishujl = {}
                                cishujl["cs_jltj"] = "成功通过 [" + \
                                    jldarr[1] + "]() " + jldarr[2] + " 次"
                                cishujl["cs_jl"] = '![' + jldarr[3] + \
                                    '](zhs/'+jldarr[3] + \
                                    'i.png) * ' + jldarr[4]
                                if(len(jldarr) > 5 and jldarr[5].find('skill=') == 0):
                                    cishujl["cs_jl"] += "(技能等级 " + \
                                        jldarr[5].replace('skill=', '')+") "
                                _h["cishujl"].append(cishujl)
    _timearrcj = re.split("==[\s]*?成就獎勵[\s]*?==([\s\S]*?)\|}", daily)  # 成就獎勵
    if len(_timearrcj) == 3:  # 循环 成就獎勵
        timecj = re_h.sub('', _timearrcj[1])  # 去掉HTML 标签
        timecj = re_comment.sub('', timecj)  # 去掉HTML注释
        t = ""
        for d in timecj.splitlines():
            if(d.rfind("獎勵=") > -1):
                t = str.strip(d.replace("成就獎勵=", "").replace("獎勵=", ""))
            d = d.replace("{{", "").replace("}}", "")
            if(d.find("成就獎勵|") == 0):
                for _h in openhis:
                    if _h["start"].find(t) == 0:
                        _lkid = getUrlParamsByName(d, "id")
                        _lknum = getUrlParamsByName(d, "num")
                        _lksoul = getUrlParamsByName(d, "soul")
                        if len(_lkid) > 0 and _lkid[0] == "C":
                            getlkimg(_lkid)
                        if _lkid.isdigit():
                            img_src = 'static/zhs/' + _lkid + 'i.png'
                            # if not os.path.exists(img_src): getzhs(_lkid)
                        _h["cj"].append({'star': d.split('|')[
                                        1], 'id': _lkid, 'soul': _lksoul, 'm': getUrlParamsByName(d, "M"), 'num': _lknum})
    _arr = re.split("==\s*{{TitleIcon[|]([\d]*)}}([\s\S]*?)==", daily)
    xarr = []
    i = 1
    while i < len(_arr):  # 循环每个副本（初级，中级等）
        stageid = _arr[i]
        stagetitle = str.strip(
            _arr[i+1].replace("{{EXTRA}}", "").replace("{{ELITE}}", ""))
        stagelist = []
        cjlist = []
        jd = ''
        for d in re.split("\s*{{(.*)}}\s*", _arr[i+2]):  # 循环副本中每个stage
            d = str.strip(d)
            if d == "":
                continue
            for dd in ('{{' + d).split('{{關卡數據'):
                dd = '關卡數據' + dd
                arr = dd.split("|")
                if arr[0] == "關卡數據注釋" and len(arr) > 1:
                    jd = replace2(d).split("|")[1]
                    tmp = re.split(r"{{([^}]*)}}", jd)
                    if len(tmp) > 2 and len(tmp[1].split('*')) > 2 and tmp[1].split('*')[1] == '技能':
                        jd = tmp[0] + tmp[1].split('*')[0] + \
                            '场景特性：' + tmp[1].split('*')[2]
                if arr[0] == "關卡數據" and len(arr) > 1:
                    d1 = analysestage(dd)
                    if 'stage' not in d1:
                        d1["stage"] = ''
                    d1["jd"] = jd
                    stagelist.append(d1)
                if arr[0].find("{{關卡成就") > -1 or arr[0].find("{{虛影世界關卡成就") > -1:
                    dd = dd.replace('關卡數據{{關卡成就|', '').replace(
                        '{{虛影世界關卡成就|', '')
                    dd = dd.replace("'''", '**').replace('{{虛影世界關卡成就|', '')
                    dd = dd.replace("{{BASEPAGENAME}}", '['+stagetitle+']()')
                    dd = re.sub(r'({{布蘭克之匙}})',
                                r'![布蘭克之匙](toswikiapic/yaoshi.png)', dd)
                    dd = re.sub(r'({{Gift[\|]布蘭克之匙[\|][^}]*}})',
                                r'![布蘭克之匙](toswikiapic/yaoshi.png)', dd)
                    dd = replace1(dd[4:])
                    cjlist = dd.split('|')
        xarr.append({"id": stageid, 'title': stagetitle,
                     'cj': cjlist, "data": stagelist})
        i = i + 3
    cjtimes = 0
    for h in openhis:
        if len(h['cj']) > 0:
            cjtimes = cjtimes + 1
    obj = {"openhis": openhis, "cjtimes": cjtimes, "stages": xarr}
    maintitle = maintitle.replace("/", "*")
    fw = open('static/stages/tmp.json', 'w', encoding='utf-8')
    json.dump(obj, fw, ensure_ascii=False, indent=2)
    fw.close()
    isdiff = compare2file('static/stages/tmp.json',
                          'static/stages/' + maintitle + '.json')
    f = open('static/ver.json', encoding='utf-8')
    v = json.loads(f.read())
    if 'recent' not in v or not isdiff:
        os.rename('static/stages/tmp.json',
                  'static/stages/' + maintitle + '.json')
        v[maintitle] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fw = open('static/ver.json', 'w', encoding='utf-8')
        json.dump(v, fw, ensure_ascii=False, indent=2)
        fw.close()
    f.close()
    print('副本结束 ======> ', fb)


def gettask(fb):
    if fb["type"] == '':
        return
    maintitle = fb["title"]
    href = "https://tos.fandom.com/zh/wiki/"+quote(fb["title"])+"?action=edit"
    if "orgtitle" in fb:
        href = "https://tos.fandom.com/zh/wiki/" + \
            quote(fb["orgtitle"])+"?action=edit"
    if fb["type"] == '旅人的記憶':
        href += '&veswitched=1'
    print('更新副本 ------> ', maintitle, fb["type"], href)
    if isLocale:
        f = open('1.html', encoding='utf-8')
        daily = f.read()
    else:
        soup = downlink(href)
        if soup == None:
            return
        ta = soup.findAll('textarea')
        if ta == None or len(ta) == 0:
            return
        daily = ta[0].string
    sectionarr = re.split(r"[^==]{2}(.*)[==$]{2}", daily)
    openhis = []
    xarr = []
    topcj = []
    stageinfo = {}
    for n in range(1, len(sectionarr), 2):
        sectionarr[n] = str.strip(sectionarr[n])
        if(sectionarr[n].startswith("==")):
            sectionarr[n] = sectionarr[n][2:]
        sectionarr[n] = str.strip(sectionarr[n])
        m = re.match(r'([\s\S]*)({{故事\|[\s\S]*)', sectionarr[n+1])
        story = ""
        if m:
            sectionarr[n+1] = m.groups()[0]
            ddd = m.groups()[1].splitlines()
            for i in range(0, len(ddd)):
                l = ddd[i]
                if l.endswith("}}") and l.count("{{") < l.count("}}"):
                    story = '\n'.join(ddd[0:i])
                    sectionarr[n+1] += "\n".join(ddd[i+1:])
                    break
        if sectionarr[n] == '開放時間記錄':
            dd = re.sub(r'{{([\d]+)\|([\d]+)}}', r'{{\1*\2}}', sectionarr[n+1])
            for d in dd.splitlines():
                if d.find("{{Event2|") == 0 or d.find("{{event2|") == 0:
                    _oarr = d.split('|')
                    _start, _end, _note = '', '', ''
                    if len(_oarr) > 1:
                        _note = _oarr[1]
                    if len(_oarr) > 2:
                        _start = _oarr[2].replace("}}", "")
                    if len(_oarr) > 3:
                        _end = _oarr[3].replace("}}", "")
                    _note = str.strip(_note)
                    _note = re.sub(r'{{C([^}]+)\*{1}([^}]*)}}',
                                   r'![C\1](lk/C\1.png)', _note)
                    _note = re.sub(r'{{([\d]+)\*{1}([^}]*)}}',
                                   r'![\1](zhs/\1i.png)', _note)
                    openhis.append({"start": str.strip(_start), "end": str.strip(
                        _end), "note": _note, 'cj': [], 'cishujl': []})
        if sectionarr[n] == '通關次數獎勵':
            sectionarr[n+1] = re_h.sub('', sectionarr[n+1])  # 去掉HTML 标签
            sectionarr[n+1] = re_comment.sub('', sectionarr[n+1])  # 去掉HTML注释
            tgjlcuarr = re.split(r'(.*)獎勵=', sectionarr[n+1])
            for m in range(1, len(tgjlcuarr), 2):
                for _h in openhis:
                    tgjlcuarr[m] = str.strip(tgjlcuarr[m])
                    # print(_h["start"], (tgjlcuarr[m]), _h["start"].find(str.strip(tgjlcuarr[m])))
                    if _h["start"].find(tgjlcuarr[m]) == 0 or _h["end"].find(tgjlcuarr[m]) == 0:
                        for d in tgjlcuarr[m+1].splitlines():
                            if(d.find("通關獎勵格") > 0):
                                if d.startswith("{{"):
                                    d = d[2:]
                                if d.endswith("}}"):
                                    d = d[:-2]
                                d = re.sub(
                                    r'{{([^}]+)\|([^}]*)}}', r'{{\1*\2}}', d)
                                d = re.sub(
                                    r'{{C([^}]+)\*{1}([^}]*)}}', r'![C\1](lk/C\1.png)', d)
                                d = re.sub(
                                    r'{{([\d]+)\*{1}([^}]*)}}', r'![\1](zhs/\1i.png)', d)
                                jldarr = d.replace("{{通關獎勵格", "").split(
                                    '|')  # 奖励召唤兽 id
                                if(jldarr[1][0:2] == 'f='):
                                    cishujl = {}
                                    cishujl["cs_jltj"] = "首次通过 [" + \
                                        jldarr[2]+"]()"
                                    if(jldarr[5].find('other=') == 0):
                                        cishujl["cs_jl"] = jldarr[5].split(
                                            "=")[1] + " * " + jldarr[6]
                                    _h["cishujl"].append(cishujl)
                                if len(jldarr) > 3:
                                    if jldarr[3] != '':
                                        cishujl = {}
                                        stagelevelname = ''
                                        if jldarr[1] == 'T':
                                            stagelevelname = '煉獄級'
                                        if jldarr[1] == 'U':
                                            stagelevelname = '地獄級'
                                        cishujl["cs_jltj"] = "成功通过 [" + \
                                            stagelevelname + "]() " + \
                                            jldarr[2] + " 次"
                                        cishujl["cs_jl"] = '![' + jldarr[3] + \
                                            '](zhs/'+jldarr[3] + \
                                            'i.png) * ' + jldarr[4]
                                        if(len(jldarr) > 5 and jldarr[5].find('skill=') == 0):
                                            cishujl["cs_jl"] += "(技能等级 " + \
                                                jldarr[5].replace(
                                                    'skill=', '')+") "
                                        _h["cishujl"].append(cishujl)
        if sectionarr[n] == '成就獎勵':
            sectionarr[n+1] = re_h.sub('', sectionarr[n+1])  # 去掉HTML 标签
            sectionarr[n+1] = re_comment.sub('', sectionarr[n+1])  # 去掉HTML注释
            cjjluarr = re.split(r'(.*)成就獎勵=', sectionarr[n+1])
            if len(cjjluarr) == 1:
                for l in sectionarr[n+1].splitlines():
                    if l.find("{{成就獎勵|") == -1:
                        continue
                    _t = l.replace("}}", "").replace("{{", "")
                    _lkid = getUrlParamsByName(_t, "id")
                    _lknum = str.strip(getUrlParamsByName(_t, "num"))
                    _lksoul = getUrlParamsByName(_t, "soul")
                    if len(_lkid) > 0 and _lkid[0] == "C":
                        getlkimg(_lkid)
                    if _lkid.isdigit():
                        img_src = 'static/zhs/' + _lkid + 'i.png'
                    topcj.append({'star': _t.split('|')[
                                 1], 'id': _lkid, 'soul': _lksoul, 'm': getUrlParamsByName(_t, "M"), 'num': _lknum})
            for m in range(1, len(cjjluarr), 2):
                for _h in openhis:
                    if _h["start"].find(cjjluarr[m]) == 0:
                        for l in cjjluarr[m+1].splitlines():
                            if l.find("{{成就獎勵|") == -1:
                                continue
                            _t = l.replace("}}", "").replace("{{", "")
                            _lkid = getUrlParamsByName(_t, "id")
                            _lknum = str.strip(getUrlParamsByName(_t, "num"))
                            _lksoul = getUrlParamsByName(_t, "soul")
                            if len(_lkid) > 0 and _lkid[0] == "C":
                                getlkimg(_lkid)
                            if _lkid.isdigit():
                                img_src = 'static/zhs/' + _lkid + 'i.png'
                            _h["cj"].append({'star': _t.split('|')[
                                            1], 'id': _lkid, 'soul': _lksoul, 'm': getUrlParamsByName(_t, "M"), 'num': _lknum})
        stagenote = ""
        if re.match(r".*{{TitleIcon\|\d+", sectionarr[n]) != None:
            _arr = re.split(
                "\s*{{TitleIcon[|]([\d]*)}}([\s\S]*?)", sectionarr[n])
            stageid = _arr[1]
            stagetitle = str.strip(_arr[3].replace(
                "{{EXTRA}}", "").replace("{{ELITE}}", ""))
            stagelist = []
            cjlist = []
            jd = ''
            # stagesplit = re.split(
            #     "<\s*tabber[^>]*>([^<]*)<\s*/\s*tabber\s*>", sectionarr[n+1])
            # stagesplit = re.split(
            #     "[\s\S]*{{地下城信息([\s\S]*){{通關獎勵}}", sectionarr[n+1])
            # stagesplit[0] = re_comment.sub('', stagesplit[0])
            # print(100*'*', stagesplit, 100*'*')
            # if len(stagesplit) == 1:
            #     stageslines = stagesplit[0].splitlines()
            # if len(stagesplit) == 3:
            #     sarr = stagesplit[1].split('|-|')
            #     stageslines = sarr[0].splitlines()
            stageslines = sectionarr[n+1].splitlines()
            for d in stageslines:
                if str.strip(d) == '':
                    continue
                if d.startswith("'''"):
                    _t = replacecommon(d)
                    stagenote += _t.replace("'''", "").replace("※''",
                                                               "※").replace('{{BASEPAGENAME}} ', '').replace('{{BASEPAGENAME}}', '').replace('{{FULLPAGENAME}} ', '').replace('{{FULLPAGENAME}}', '')
                    stagenote = str.strip(stagenote)
                if d.startswith("{{"):
                    d = d[2:]
                if d.endswith("}}"):
                    d = d[:-2]
                if d.find("地下城信息|") == 0:
                    _t1 = replace2(d.replace("地下城信息|", ""))
                    stageinfo = {}
                    for _str in _t1.split("|"):
                        stageinfo[_str.split("=")[0]] = _str.split("=")[1]
                if d.find("關卡數據注釋|") == 0:
                    jd = replace2(d.replace("關卡數據注釋|", ""))
                    tmp = re.split(r"{{([^}]*)}}", jd)
                    if len(tmp) > 2 and len(tmp[1].split('*')) > 2 and tmp[1].split('*')[1] == '技能':
                        jd = tmp[0] + tmp[1].split('*')[0] + \
                            '场景特性：' + tmp[1].split('*')[2]
                if d.find("關卡數據|") == 0:
                    d = re_comment.sub('', d)
                    d1 = analysestage(d)
                    if 'stage' not in d1:
                        d1["stage"] = ''
                    d1["jd"] = jd
                    stagelist.append(d1)
                if d.find("關卡成就|") > -1 or d.find("虛影世界關卡成就") > -1:
                    gkcjsplit = re.split(r"{{關卡成就\|([^}*]*)", d)
                    if len(gkcjsplit) > 2:
                        cjlist.append(
                            "<span style=\"font-size:12pt; font-weight:800; color:#FF5733;\">" + gkcjsplit[0] + "</span> <br>" + "<br>".join(gkcjsplit[1].split('|')))
                    else:
                        dd = d.replace('關卡成就|', '').replace('虛影世界關卡成就|', '')
                        dd = dd.replace("'''", '**')
                        dd = dd.replace("{{BASEPAGENAME}}",
                                        '['+stagetitle+']()')
                        dd = re.sub(r'({{布蘭克之匙}})',
                                    r'![布蘭克之匙](toswikiapic/yaoshi.png)', dd)
                        dd = re.sub(r'({{Gift[\|]布蘭克之匙[\|][^}]*}})',
                                    r'![布蘭克之匙](toswikiapic/yaoshi.png)', dd)
                        dd = re.sub(
                            r'({{金幣}})', r'![金幣](toswikiapic/金幣.png)', dd)
                        dd = replace1(dd)
                        cjlist = dd.split("|")
            xarr.append({"id": stageid, 'title': stagetitle, "note": stagenote, "story": story,
                         'cj': cjlist, "info": stageinfo, "data": stagelist})
    obj = {"openhis": openhis, "cj": topcj, "stages": xarr}
    maintitle = maintitle.replace("/", "*")
    if fb["type"] == '虛影世界' or fb["type"] == '旅人的記憶' or fb["type"] == '主線':
        fw = open('static/stages/'+maintitle+'.json', 'w', encoding='utf-8')
        json.dump(obj, fw, ensure_ascii=False, indent=2)
        fw.close()
    else:
        fw = open('static/stages/tmp.json', 'w', encoding='utf-8')
        json.dump(obj, fw, ensure_ascii=False, indent=2)
        fw.close()
        isdiff = compare2file('static/stages/tmp.json',
                              'static/stages/' + maintitle + '.json')
        f = open('static/ver.json', encoding='utf-8')
        v = json.loads(f.read())
        if 'recent' not in v or not isdiff:
            os.rename('static/stages/tmp.json',
                      'static/stages/' + maintitle + '.json')
            v[maintitle] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            fw = open('static/ver.json', 'w', encoding='utf-8')
            json.dump(v, fw, ensure_ascii=False, indent=2)
            fw.close()
        f.close()
    print('副本结束 ======> ', fb)


def getmainline(allupdate):
    href = "https://tos.fandom.com/zh/wiki/Template:" + \
        quote("主線任務")+"?action=edit"
    soup = downlink(href)
    if soup == None:
        return
    textarea = soup.findAll('textarea')[0].string
    # f =open('2.txt', encoding='utf-8')
    # textarea=f.read()
    sections = re.search(
        r"<div class=\"rstage\".*><tabber>([\s\S]+?)<\/tabber>", textarea)
    d = re.sub(r'([^\s]*)=', r'# \1', sections.group(1))
    d = re.sub(r"<center>'''([^']*)'''</center>", r'### \1', d)
    d = re.sub(r"'''([^']*)'''", r'\1', d)
    stagegroup = re.split(r"{{DIcon\|[^\|]*\|([^\|]*).*", d)
    xuyingstages = []
    for i in range(1, len(stagegroup), 2):
        stagename = str.strip(stagegroup[i])
        xuyingstages.append(stagename)
        fb = {'title': stagename, 'type': '主線'}
        if not os.path.exists('static/stages/' + stagename + '.json') or allupdate:
            gettask(fb)
    d = re.sub(r"\((.+?)\)", r'#\1', d)
    # print(d, "-----")
    d = re.sub(r"{{DIcon\|([^\|]*)\|([^\|]*).*", r'![\2](\1) [\2](\2)', d)
    dd = ""
    dg = []
    for ll in d.splitlines():
        ll = str.strip(ll)
        if ll == '' or ll == '|-|' or ll == '----':
            continue
        if ll[0] == "!":
            va = re.split("(\(.+?\))", ll)
            if va[1][1] == "-":
                va[1] = "S" + va[1][1:-1]
            else:
                va[1] = va[1][1:-1]
            va[1] = "(fbimg/" + va[1] + "i.png)"
            va[len(va) - 2] = "(/pages/index/detail/detail?name=" + \
                urllib.parse.quote(va[len(va) - 2][1:-1]) + ")"
            ll = "".join(va)
        dd += ll + "\n"
        if ll[0] == '#' and ll[1] == ' ':
            o = {"title": ll[2:], "data": ""}
            if dd != '':
                dg.append(o)
        # if(ll.startswith("### ")):
        #     ll = ll[4:]
        # if(ll.startswith("# ")):
        #     ll = ll[2:]
        o["data"] += ll + "\n"
    for dggg in dg:
        # print(dggg["data"].find("###"), dggg["data"])
        dggg["data"] = "\n".join(dggg["data"].split("\n")[1:])
    fw = open('static/mainline.txt', 'w', encoding='utf-8')
    fw.write(json.dumps(dg, ensure_ascii=False, indent=2))
    fw.close()
    fw = open('static/mainlinestages2.txt', 'w', encoding='utf-8')
    fw.write(json.dumps(xuyingstages, ensure_ascii=False, indent=2))
    fw.close()


def getmainline1():
    download_url = "https://tos.fandom.com/zh/wiki/Template:%E4%B8%80%E8%87%B3%E4%B8%83%E5%B0%81%E9%97%9C%E5%8D%A1%E6%95%B8%E6%93%9A?action=edit"
    soup = downlink(download_url)
    if soup == None:
        return
    textarea = soup.findAll('textarea')[0].string
    sections = re.split(r'\|-', textarea)
    mainline = []
    d = []
    sectionpfix = str.strip(sections[1].split('|')[1].split('-')[1])
    for sec in sections[2].splitlines():
        if str.strip(sec) == '':
            continue
        section = {"name": "", "data": []}
        if sec[0] == '!':
            section["name"] = sec[1:]
        d.append(section)
    secidx = 4
    while secidx < len(sections):
        lineid = 0
        for line in sections[secidx].splitlines():
            if str.strip(line) == '' or line.find('|{{DIcon|') != 0:
                continue
            _a = line.split('|')
            title = _a[3]
            img = _a[2]+"i.png"
            d[lineid]["data"].append(
                {'title': title, 'type': '主线', 'img': img})
            lineid += 1
        secidx += 2
    mainline.append({"name": sectionpfix, "data": d})

    # 八封關卡數據
    download_url = "https://tos.fandom.com/zh/wiki/Template:%E5%85%AB%E5%B0%81%E9%97%9C%E5%8D%A1%E6%95%B8%E6%93%9A?action=edit"
    soup = downlink(download_url)
    if soup == None:
        return
    textarea = soup.findAll('textarea')[0].string
    sections = re.split(r'\|-', textarea)
    sectionpfix = str.strip(sections[1].split('|')[1].split('-')[1])
    d = []
    for sec in sections[2].splitlines():
        if str.strip(sec) == '':
            continue
        section = {"name": "", "data": []}
        if sec[0] == '!':
            section["name"] = sec.split("|")[1]
        d.append(section)
    lineid = 0
    for line in sections[3].splitlines():
        if str.strip(line) == '':
            continue
        _a = re.split(r'{{(DIcon.+?)}}+?', line)
        if(len(_a) == 1):
            continue
        for _a1 in _a:
            if _a1.find('DIcon') == 0:
                title = _a1.split('|')[2]
                img = _a1.split('|')[1]+"i.png"
                d[lineid]["data"].append(
                    {'title': title, 'type': '主线', 'img': img})
        lineid += 1
    mainline.append({"name": sectionpfix, "data": d})

    # 九封關卡數據
    download_url = "https://tos.fandom.com/zh/wiki/Template:%E4%B9%9D%E5%B0%81%E9%97%9C%E5%8D%A1%E6%95%B8%E6%93%9A?action=edit"
    soup = downlink(download_url)
    if soup == None:
        return
    textarea = soup.findAll('textarea')[0].string
    sections = re.split(r'\|-', textarea)
    sectionpfix = str.strip(sections[1].split('|')[1].split('-')[1])
    d = []
    for sec in sections[2].splitlines():
        if str.strip(sec) == '':
            continue
        section = {"name": "", "data": []}
        if sec[0] == '!':
            section["name"] = sec.split("|")[1]
        d.append(section)
    lineid = 0
    for line in sections[3].splitlines():
        if str.strip(line) == '':
            continue
        _a = re.split(r'{{(DIcon.+?)}}+?', line)
        if(len(_a) == 1):
            continue
        for _a1 in _a:
            if _a1.find('DIcon') == 0:
                title = _a1.split('|')[2]
                img = _a1.split('|')[1]+"i.png"
                d[lineid]["data"].append(
                    {'title': title, 'type': '主线', 'img': img})
        lineid += 1
    lineid = 0
    for line in sections[4].splitlines():
        if str.strip(line) == '':
            continue
        _a = re.split(r'{{(DIcon.+?)}}+?', line)
        if(len(_a) == 1):
            continue
        for _a1 in _a:
            if _a1.find('DIcon') == 0:
                title = _a1.split('|')[2]
                img = _a1.split('|')[1]+"i.png"
                d[lineid]["data"].append(
                    {'title': title, 'type': '主线', 'img': img})
        lineid += 1
    mainline.append({"name": sectionpfix, "data": d})

    # 十封關卡數據
    download_url = "https://tos.fandom.com/zh/wiki/Template:%E5%8D%81%E5%B0%81%E9%97%9C%E5%8D%A1%E6%95%B8%E6%93%9A?action=edit"
    soup = downlink(download_url)
    if soup == None:
        return
    textarea = soup.findAll('textarea')[0].string
    sections = re.split(r'\|-\s\!width=100% colspan=6', textarea)
    m = re.search('\[\[主線任務\]\](.*)\s', textarea)
    if m:
        sectionpfix = str.strip(m.group(0).split('-')[1])
    d = []
    for section in sections[1:]:
        seclist = []
        lines = section.splitlines()
        title = lines[0].split('|')[1]
        sectionobj = {"name": title, "data": []}
        lineid = 0
        dlid = 0
        for line in lines:
            if str.strip(line) == '':
                continue
            _a = re.split(r'{{(DIcon.+?)}}+?', line)
            if(len(_a) > 1):
                for _a1 in _a:
                    if _a1.find('DIcon') == 0:
                        _title = _a1.split('|')[2]
                        _img = _a1.split('|')[1]+"i.png"
                        seclist.append(
                            {'title': _title, 'type': '主线', 'img': _img})
            else:
                if line.find("|{{") == 0:
                    _temp = re.split('[^{]*{{(\d+)\|\d+}}', line)
                    _temp = list(filter(not_empty, _temp))
                    seclist[dlid]["dl"] = ",".join(_temp)
                    dlid += 1
            lineid += 1
        sectionobj["data"] = seclist
        d.append(sectionobj)

    # 十一封關卡數據
    download_url = "https://tos.fandom.com/zh/wiki/Template:%E5%8D%81%E4%B8%80%E5%B0%81%E9%97%9C%E5%8D%A1%E6%95%B8%E6%93%9A?action=edit"
    soup = downlink(download_url)
    if soup == None:
        return
    textarea = soup.findAll('textarea')[0].string
    sections = re.split(r'\|-\s\!width=100% colspan=6', textarea)
    m = re.search('\[\[主線任務\]\](.*)\s', textarea)
    if m:
        sectionpfix = str.strip(m.group(0).split('-')[1])
    d = []
    for section in sections[1:]:
        seclist = []
        lines = section.splitlines()
        title = lines[0].split('|')[1]
        sectionobj = {"name": title, "data": []}
        lineid = 0
        dlid = 0
        for line in lines:
            if str.strip(line) == '':
                continue
            _a = re.split(r'{{(DIcon.+?)}}+?', line)
            if(len(_a) > 1):
                for _a1 in _a:
                    if _a1.find('DIcon') == 0:
                        _title = _a1.split('|')[2]
                        _img = _a1.split('|')[1]+"i.png"
                        seclist.append(
                            {'title': _title, 'type': '主线', 'img': _img})
            else:
                if line.find("|{{") == 0:
                    _temp = re.split('[^{]*{{(\d+)\|\d+}}', line)
                    _temp = list(filter(not_empty, _temp))
                    seclist[dlid]["dl"] = ",".join(_temp)
                    dlid += 1
            lineid += 1
        sectionobj["data"] = seclist
        d.append(sectionobj)
    mainline.append({"name": sectionpfix, "data": d})
    fw = open('static/mainline.json', 'w', encoding='utf-8')
    json.dump(mainline, fw, ensure_ascii=False, indent=2)
    getfbimg("主線任務")


def getUrlParamsByName(t, name):
    _arr = re.split("(^|\|)(" + name + "=[^\|]*)(\||$)", t)
    for a in _arr:
        if a.find(name+'=') > -1:
            return a.replace(name+'=', '')
    return ''


def analysestage(d):
    print(d)
    # d=re_br.sub('', d)#将br转换为换行
    # d=re_h.sub('', d) #去掉HTML 标签
    # d=re_comment.sub('', d)#去掉HTML注释
    # turn=1{{初始CD|1}} ==> turn=1(1)
    d = re.sub(r'\|turn=(\d?){{初始CD\|(\d?)}}', r'|turn=\1(\2)', d)
    d = re.sub(r'\|turn=(\d?)\(\)', r'|turn=\1', d)  # turn=1() ==> turn=1
    d = re.sub(r'{{([^}]+)[\|]([^}]{0,})[\|]([^}]+)}}', r'{{\1*\2*\3}}', d)
    d = re.sub(r'{{([^}]+)[\|]([^}]{0,})}}', r'{{\1*\2}}', d)
    _darr = re.split("es=[|]note=([\s\S]*)", d)
    if len(_darr) == 3 and _darr[1] != '':
        d = (_darr[0] + 'es=' + _darr[1].split('<br>')
             [1].replace("{{", "").replace("}}", "").replace("ES", ""))
    note = ""
    notesplit = re.split("\|note=([\s\S]*)", d)
    if len(notesplit) > 1:
        note = notesplit[1]
        d = re.compile("\|note=([\s\S]*)").sub('', d)
    darr = d.split('|')
    card = darr[1]
    if(card.find("=") > -1):
        card = darr[2]
    dval = {}
    temparr = []
    dval["card"] = card
    for item in darr[1:]:
        if item == '':
            continue
        _tmp = item.split('=')
        if len(_tmp) == 2:
            dval[_tmp[0]] = _tmp[1]
    dval["note"] = note
    dval["esjson"] = None
    for _tmp in dval:
        if(_tmp == "stage"):  # 掉落银，金卡
            img_src = 'common/银卡.png'
            if not os.path.exists('static/' + img_src):
                downimg('https://static.wikia.nocookie.net/tos/images/2/2f/%E9%8A%80%E5%8D%A1.png/revision/latest/scale-to-width-down/13?cb=20150108102345&path-prefix=zh', 'static/' + img_src)
            img_src = 'common/白金卡.png'
            if not os.path.exists('static/' + img_src):
                downimg('https://static.wikia.nocookie.net/tos/images/b/b2/%E7%99%BD%E9%87%91%E5%8D%A1.png/revision/latest/scale-to-width-down/13?cb=20190529132539&path-prefix=zh', 'static/' + img_src)
            img_src = 'common/金卡.png'
            if not os.path.exists('static/' + img_src):
                downimg('https://static.wikia.nocookie.net/tos/images/8/83/%E9%87%91%E5%8D%A1.png/revision/latest/scale-to-width-down/13?cb=20190529132644&path-prefix=zh', 'static/' + img_src)
        if(_tmp == "card" or _tmp == "drop") and dval[_tmp] != '':  # 敌人及掉落图片
            img_src = 'zhs/' + dval[_tmp] + 'i.png'
            if not os.path.exists('static/' + img_src) and not isLocale:  # getmainlineimg
                print(img_src + "图片不存在" + dval[_tmp])
                getmainlineimg(dval[_tmp])
                getzhs(dval[_tmp])
        if(_tmp == "es" and dval[_tmp] != '' and not isLocale):  # 技能
            esjson = getes(dval[_tmp])
            dval["esjson"] = esjson
        if(_tmp == "chest"):  # 王关金币
            getchest()
    return dval


class TestClass():
    def __init__(self):
        # 线程池+线程同步改造添加代码处1/5： 定义锁和线程池
        # 我们第二大节中说的是锁不能在线程类内部实例化，这个是调用类不是线程类，所以可以在这里实例化
        self.threadLock = threading.Lock()
        # 定义2个线程的线程池
        self.thread_pool = ThreadPoolExecutor(2)
        # 定义2个进程的进程池。进程池没用写在这里只想表示进程池的用法和线程池基本一样
        # self.process_pool = ProcessPoolExecutor(2)
        pass

    def getallzhs(self, phase):
        if not os.path.exists('static/allzhsgroup.json') or os.path.getsize('static/allzhsgroup.json') == 0:
            phs = []
        else:
            with open('static/allzhsgroup.json', 'r') as json_file:
                if json_file != '':
                    phs = json.load(json_file)
        if phs.count(phase) == 0:
            phs.append(phase)
            fw1 = open('static/allzhsgroup.json', 'w', encoding='utf-8')
            fw1.write(json.dumps(phs, ensure_ascii=False, indent=2))
            fw1.close()

        download_url = "http://tos.fandom.com/zh/wiki/%E5%9C%96%E9%91%92/" + \
            quote(phase)
        soup = downlink(download_url)
        if soup == None:
            return
        div = soup.findAll('div', class_='mw-parser-output')
        tds = div[0].findAll("table")[0].findAll('td')
        if not os.path.exists('static/allzhs'+phase+'.json') or os.path.getsize('static/allzhs'+phase+'.json') == 0:
            dic = []
        else:
            with open('static/allzhs'+phase+'.json', 'r') as json_file:
                if json_file != '':
                    dic = json.load(json_file)
        self.threadLock = threading.Lock()
        # 定义2个线程的线程池
        self.thread_pool = ThreadPoolExecutor(50)
        tasks = []
        begin = time.time()
        for td in tds:
            tasks.append(self.thread_pool.submit(self.getsinglezhs, td))
        for future in as_completed(tasks):
            data = future.result()
            if not data:
                continue
            _t = False
            for item in dic:
                if item["id"] == data["id"]:
                    _t = True
                    break
            if not _t:
                dic.append(data)
        times = time.time() - begin
        fw = open('static/allzhs'+phase+'.json', 'w', encoding='utf-8')
        model = json.dumps(dic, ensure_ascii=False, indent=2)
        fw.write(model)
        fw.close()
        pass

    def getsinglezhs(self, td):
        # zhsobj = {}
        if td.div == None:
            return
        img = td.div.a.img
        zshname = img.get("data-image-name")
        id = zshname.replace('i.png', '')
        downsrc = img.get("data-src")
        if downsrc == None:
            downsrc = img.get("src")
        if zshname == '000i.png':
            return
        thread_name = threading.current_thread().name
        # 线程池+线程同步改造添加代码处4/5： 获取锁
        self.threadLock.acquire()
        self.threadLock.release()
        img_src = 'static/zhs/' + zshname
        if downimg(downsrc, img_src):  # and id not in dic:
            zhsobj = {'id': id, 'path': img_src}
        if not os.path.exists('static/zhs/' + id + ".json") or True:
            getzhs(id)
        return zhsobj

    def mergeallzhs(self):
        tags = {}
        tj = {"rare": [], "tag": []}
        allzhs = []
        with open('static/allzhsgroup.json', 'r') as json_file1:
            if json_file1 != '':
                dictgroup = json.load(json_file1)
                series = []
                for g in dictgroup:
                    if os.path.exists('static/allzhs'+g+'.json') and os.path.getsize('static/allzhs'+g+'.json') > 0:
                        with open('static/allzhs'+g+'.json', 'r') as json_file:
                            if json_file != '':
                                dic = json.load(json_file)
                                dic = [x for x in dic if x != None]
                                for zhs in dic:
                                    if zhs == None:
                                        continue
                                    if not os.path.exists('static/zhs/' + zhs["id"] + '.json'):
                                        continue
                                    with open('static/zhs/' + zhs["id"] + '.json', 'r') as zhs_file:
                                        if zhs_file != '':
                                            zhsobj = json.load(zhs_file)
                                            del zhsobj["stage"]
                                            if 'story' in zhsobj:
                                                del zhsobj["story"]
                                            zhs["rare"] = zhsobj["rare"]
                                            zhs["attr"] = zhsobj["attr"]
                                            zhs["race"] = zhsobj["race"]
                                            zhs["series"] = zhsobj["series"]
                                            zhs["skill"] = "" if "skill" not in zhsobj else zhsobj["skill"]
                                            zhs["lskill"] = "" if "lskill" not in zhsobj else zhsobj["lskill"]
                                            # zhs["detail"] = {
                                            #     "name": zhsobj["name"], "attr": zhsobj["attr"], "series": zhsobj["series"], "skill": "" if "skill" not in zhsobj else zhsobj["skill"], "lskill": "" if "lskill" not in zhsobj else zhsobj["lskill"]}
                                            if(zhsobj["rare"] not in tj["rare"]):
                                                tj["rare"].append(
                                                    zhsobj["rare"])
                                            seri = zhsobj["series"]
                                            if series.count(seri) == 0:
                                                series.append(seri)
                                            # if "display" not in zhsobj or ("display" in zhsobj and zhsobj["display"][0]=='S'):
                                                # print(zhsobj["id"], zhsobj["display"])
                                            if ("display" not in zhsobj or zhsobj["display"][0]!='S') and "skill" in zhsobj and os.path.exists('static/skill/' + zhsobj["skill"] + '.json'):
                                                with open('static/skill/' + zhsobj["skill"] + '.json', 'r') as skill_file:
                                                    if skill_file != '':
                                                        skill_effectobj = json.load(
                                                            skill_file)
                                                        if "tags" not in zhs:
                                                            zhs["tags"] = []
                                                        if "effect" in skill_effectobj:
                                                            t1(zhsobj,
                                                            skill_effectobj["effect"], zhs, tags)
                                            if ("display" not in zhsobj or zhsobj["display"][0]!='S') and "skill2" in zhsobj and os.path.exists('static/skill/' + zhsobj["skill2"] + '.json'):
                                                with open('static/skill/' + zhsobj["skill2"] + '.json', 'r') as skill_file:
                                                    if skill_file != '':
                                                        skill_effectobj = json.load(
                                                            skill_file)
                                                        if "tags" not in zhs:
                                                            zhs["tags"] = []
                                                        if "effect" in skill_effectobj:
                                                            t1(zhsobj,
                                                            skill_effectobj["effect"], zhs, tags)
                                dict = sorted(dic, key=(lambda item: item != None) and (
                                    lambda item: item["id"]))
                                fw = open('static/allzhslist'+g +
                                          '.json', 'w', encoding='utf-8')
                                model = json.dumps(
                                    dict, ensure_ascii=False, indent=2)
                                fw.write(model)
                                fw.close()
                                allzhs += dict
                fw = open('static/zhsseries.json', 'w', encoding='utf-8')
                model = json.dumps(series, ensure_ascii=False, indent=2)
                fw.write(model)
                fw.close()
                fw = open('static/zhstags.json', 'w', encoding='utf-8')
                model = json.dumps(tags, ensure_ascii=False, indent=2)
                fw.write(model)
                fw.close()
                for tag in tags:
                    fw = open('static/tags/'+tag+'.json',
                              'w', encoding='utf-8')
                    if tag not in tj["tag"]:
                        tj["tag"].append(tag)
                    model = json.dumps(tags[tag], ensure_ascii=False, indent=2)
                    fw.write(model)
                    fw.close()
                tj["rare"].sort()
                fw = open('static/zhstj.json', 'w', encoding='utf-8')
                model = json.dumps(tj, ensure_ascii=False, indent=2)
                fw.write(model)
                fw.close()
                for obj in allzhs:
                    if 'orgin' in obj: del obj["orgin"]
                    if 'path' in obj: del obj["path"]
                    if 'skill' in obj: del obj["skill"]
                    if 'lskill' in obj: del obj["lskill"]
                fw = open('static/monster_JSON1.json', 'w', encoding='utf-8')
                model = json.dumps(allzhs, ensure_ascii=False, indent=2)
                fw.write(model)
                fw.close()


def t1(zhsobj, skill_effect, zhs, tags):
    # dict = [["引爆", "引爆"], ["回復力提升", "增回"],
    #         ["吸取|生命力", "回血"], ["恢復生命力", "回血"], ["回復|生命力", "回血"], ["吸取|生命力", "回血"], ["符石掉落率提升", "符石掉落率提升"], ["強化符石的效果提升", "強化珠效果提升"], ["所受傷害減少", "減傷"], ["敵人的防禦力減", "破防"], ["攻擊力提升", "增攻"], ["全隊攻擊力|愈高", "增攻"], ["主動技能|變為", "主動技改變"], ["計算多 1 連擊 (Ex. Combo)", "增加Ex.Combo"], ["組合技能", "組合技能"], ["", ""], ["生命力提升", "增血"], ["無法行動", "無法行動"], ["轉為|屬性", "敵方轉屬"], ["凍結敵方", "凍結敵方"], ["心符石兼具|屬性符石效果", "心兼具其他"], ["兼具所有屬性符石效果", "符石兼具水"], ["兼具所有屬性符石效果", "符石兼具火"], ["兼具所有屬性符石效果", "符石兼具木"], ["兼具所有屬性符石效果", "符石兼具光"], ["兼具所有屬性符石效果", "符石兼具暗"], ["兼具水符石", "符石兼具水"], ["兼具火符石", "符石兼具火"], ["兼具木符石", "符石兼具木"], ["兼具光符石", "符石兼具光"], ["兼具暗符石", "符石兼具暗"], [
    #     "任意移動符石而不會發動消除", "排珠"], ["被寄生", "寄生敵方"], ["敵方全體中毒", "敵方中毒"], ["攻擊力有機會提升", "爆擊"], ["可以合體", "合體"], ["主動技能 CD 減少", "永久減CD"], ["技能 CD 減少", "永久減CD"], ["目標無法行動", "無法行動"], ["石化敵方", "石化敵方"], ["引爆", "引爆"], ["直接引爆水符石", "水符石引爆"], ["直接引爆火符石", "火符石引爆"], ["直接引爆木符石", "木符石引爆"], ["直接引爆光符石", "光符石引爆"], ["直接引爆暗符石", "暗符石引爆"], ["直接引爆水屬性以外的符石", "水外符石引爆"], ["直接引爆火屬性以外的符石", "火外符石引爆"], ["直接引爆木屬性以外的符石", "木外符石引爆"], ["直接引爆光屬性以外的符石", "光外符石引爆"], ["直接引爆暗屬性以外的符石", "暗外符石引爆"], ["兼具隊長技能", "兼具隊長技能"], ["所有符石隨機轉換", "大幅轉版"], ["以回血溢出值作|攻擊", "溢補攻擊"], ["所受傷害不會使你死亡", "意志"], ["召喚獸的屬性轉換為", "召喚獸轉"], ["攻擊力減至", "我方減攻"], ["將被減去的攻擊力加入自身攻擊力", "我方攻擊力吸收"], ["攻擊力會優先跟隨", "攻擊力共鳴"], ["敵方全體點燃", "點燃敵方"], ["敵方所受傷害|轉化為我方生命力", "我方傷害吸收"], ["敵方互相或自我|攻擊", "魅惑敵方"], ["我方回復力減至", "我方減回"], ["受到的傷害提升", "我方受傷增加"], ["符石掉落機率提升", "改變掉落機率"], ["進入關卡後|技能 CD 減少", "進場減CD"], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""]]
    # dict.extend([["造成|屬性傷害", "直傷"], ["進行|屬性攻擊", "直傷"], ["對敵方全體造成無屬性傷害", "直傷"], [
    #             "對敵方全體造成傷害", "直傷"], ["造成|屬性傷害|傷害無視防禦力", "破防直傷"]])
    # dict.extend([["心符石轉化為", "心轉其他"], ["轉化為水符石", "符石轉水"], ["轉化為火符石", "符石轉火"], ["轉化為木符石", "符石轉木"], ["轉化為光符石", "符石轉光"], ["轉化為暗符石", "符石轉暗"], ["轉化為|強化符石", "符石強化"], ["轉化為|水強化符石", "符石轉水強化"], ["轉化為|火強化符石", "符石轉火強化"], [
    #             "轉化為|木強化符石", "符石轉木強化"], ["轉化為|光強化符石", "符石轉光強化"], ["轉化為|暗強化符石", "符石轉暗強化"], ["轉化為心符石", "符石轉心"], ["木符石轉化為", "木轉其他"], ["火符石轉化為", "火轉其他"], ["木符石轉化為", "木轉其他"], ["光符石轉化為", "光轉其他"], ["暗符石轉化為", "暗轉其他"]])
    # dict.extend([["傷害持續提升", "增傷"], ["攻擊力|倍", "增傷"],  ["攻擊力|提升", "增傷"], [
    #             "攻擊力愈高", "增傷"], ["加入自身攻擊力", "增傷"], ["提升全隊攻擊力", "增傷"], ["全隊攻擊力提升", "增傷"]])
    # dict.extend([["生命力、攻擊力、回復力 2 倍", "增攻"], [
    #             "生命力、攻擊力、回復力 2 倍", "增回"], ["生命力、攻擊力、回復力 2 倍", "增血"]])
    # dict.extend([["暈擊敵方", "暈擊敵方"]])
    # dict.extend([["造成的最大傷害轉換為全隊神族及魔族的傷害", "共鳴"], ["攻擊力會優先跟隨", "攻擊力共鳴"]])
    # dict.extend([["全隊追打", "全隊追打"], ["全隊追打火屬性攻擊", "火屬追打"]])

    # dict.extend([["不能對敵方造成傷害", "限制成員攻擊"]])

    zhs["skill"] = skill_effect
    skill_effect = skill_effect.replace("<br>", "")
    skill_effect = skill_effect.replace("&nbsp;", "")
    for item in filterdict.dict:
        key = item[0]
        value = item[1]
        if key == '' or value == '':
            continue
        t = True
        for item2 in key.split("|"):
            if t and skill_effect.find(item2) == -1:
                t = False
        if t and value not in zhs["tags"]:
            zhs["tags"].append(value)
            if zhs["id"] == "131":
                print(skill_effect, zhs["tags"])
        if t:
            if value not in tags:
                tags[value] = []
            aexists = False
            for item2 in tags[value]:
                if zhsobj["id"] == item2["id"]:
                    aexists = True
                    break
            if not aexists:
                tags[value].append(
                    {"id": zhsobj["id"], "rare": zhsobj["rare"], "attr": zhsobj["attr"], "race": zhsobj["race"], "series": zhsobj["series"]})


def convertalzhs():
    if not os.path.exists('static/allzhs1.json') or os.path.getsize('static/allzhs1.json') == 0:
        dic = {}
    else:
        with open('static/allzhs1.json', 'r') as json_file:
            if json_file != '':
                dic = json.load(json_file)
    if '3' not in dic:
        dic['3'] = {'id': '000', 'orgin': '', 'path': ''}
        fw = open('static/allzhs1.json', 'w', encoding='utf-8')
        model = json.dumps(dic, ensure_ascii=False, indent=2)
        fw.write(model)
        fw.close()


def getlvrenbyapi(allupdate):
    download_url = "https://tos.fandom.com/zh/api.php?action=parse&format=json&text=%7B%7B%E6%97%85%E4%BA%BA%E7%9A%84%E8%A8%98%E6%86%B6%7D%7D"
    html = downurl(download_url)
    # f =open('1.html', encoding='utf-8')
    # html=f.read()
    data = json.loads(html)
    soup = BeautifulSoup(data["parse"]["text"]["*"], "lxml")
    textarea = soup.findAll('div', class_='mobileHide')[0]
    d = []
    sectiontitle = ""
    sectionobj = {"title": "", "islosed": "0",
                  "type": "旅人的記憶", "note": "", "stages": []}
    for div in textarea.children:
        if isinstance(div, bs4.element.Tag):  # 排除非标签元素干扰
            for div2 in div.children:
                if div2 == None:
                    continue
                if div2.name == None:
                    if div2.find("永久關閉") > -1 or div2.find("香港") > -1:
                        sectionobj["islosed"] = "1"
                    if sectionobj["note"] != '':
                        sectionobj["note"] += "\n"
                    sectionobj["note"] += str.strip(div2)
                    continue
                if "class" in div2.attrs and div2.attrs["class"][0] == 'titleBar2':
                    if sectionobj["title"] != '':
                        d.append(sectionobj)
                        sectionobj = {"title": "", "islosed": "0",
                                      "type": "旅人的記憶", "note": "", "stages": []}
                    sectionobj["title"] = str.strip(div2.text)
                if div2.name == 'div' and 'class' not in div2.attrs:
                    title = div2.a.attrs["title"]
                    imgsrc = div2.a.img.get('data-src')
                    dataimagename = div2.a.img.get('data-image-name')
                    if imgsrc == None:
                        imgsrc = div2.a.img.get('src')
                    downimg(imgsrc, 'static/fbimg/' + dataimagename)
                    sectionobj["stages"].append(
                        {"title": title, "img": dataimagename})
                    if not os.path.exists('static/stages/' + title + '.json') or allupdate:
                        gettask(
                            {"title": title, "img": dataimagename, "type": "旅人的記憶"})
    fw = open('static/lvren.json', 'w', encoding='utf-8')
    model = json.dumps(d, ensure_ascii=False, indent=2)
    fw.write(model)
    fw.close()


def getlvren():
    download_url = "https://tos.fandom.com/zh/wiki/%E6%97%85%E4%BA%BA%E7%9A%84%E8%A8%98%E6%86%B6?action=edit"
    soup = downlink(download_url)
    if soup == None:
        return
    textarea = soup.findAll('textarea')[0].string
    # f =open('1.html', encoding='utf-8')
    # textarea=f.read()
    sections = re.split(r"=='''(.*)'''==", textarea)
    d = []
    islosed = 0
    for sec in sections:
        secobj = {}
        for secline in sec.splitlines():
            if secline.find("已關閉") > -1:
                islosed = 1
            if secline.find("===") == 0:
                if("title" in secobj and "stages" in secobj and len(secobj["stages"]) > 0):
                    d.append(secobj)
                sectitle = secline.replace("===", "")
                secobj = {"title": sectitle, "islosed": islosed,
                          'type': '旅人的記憶', "stages": []}
            if secline.find("{{DIcon") == 0:
                _a1 = secline.replace("{{", "").replace("}}", "")
                title = _a1.split('|')[2]
                img = _a1.split('|')[1]+"i.png"
                if img[0] == "-":
                    img = "S" + img
                fb = {'title': title, 'img': img}
                secobj["stages"].append(fb)
                gettask(fb)
        if("title" in secobj and "stages" in secobj and len(secobj["stages"]) > 0):
            d.append(secobj)
        secobj = {}
    fw = open('static/lvren.json', 'w', encoding='utf-8')
    model = json.dumps(d, ensure_ascii=False, indent=2)
    fw.write(model)
    fw.close()
    getfbimg("旅人的记忆")


def getxuyingbyapi():
    download_url = "https://tos.fandom.com/zh/api.php?action=parse&format=json&text=%7B%7B%E8%99%9B%E5%BD%B1%E4%B8%96%E7%95%8C%7D%7D"
    # html = downurl(download_url)
    f = open('1.html', encoding='utf-8')
    html = f.read()
    data = json.loads(html)
    soup = BeautifulSoup(data["parse"]["text"]["*"], "lxml")
    textarea = soup.findAll('div', class_='module')[0]
    d = []
    sectiontitle = ""
    sectionobj = {"title": "", "islosed": "0",
                  "type": "虛影世界", "note": "", "stages": []}
    for div in textarea.children:
        if isinstance(div, bs4.element.Tag):  # 排除非标签元素干扰

            for div2 in div.children:
                if div2 == None:
                    continue
                if div2.name == None:
                    if div2.find("永久關閉") > -1 or div2.find("香港") > -1:
                        sectionobj["islosed"] = "1"
                    if sectionobj["note"] != '':
                        sectionobj["note"] += "\n"
                    sectionobj["note"] += str.strip(div2)
                    continue
                if "class" in div2.attrs and div2.attrs["class"][0] == 'titleBar2':
                    if sectionobj["title"] != '':
                        d.append(sectionobj)
                        sectionobj = {"title": "", "islosed": "0",
                                      "type": "虛影世界", "note": "", "stages": []}
                    sectionobj["title"] = str.strip(div2.text)
                if div2.name == 'div' and 'class' not in div2.attrs:
                    title = div2.a.attrs["title"]
                    imgsrc = div2.a.img.get('data-src')
                    dataimagename = div2.a.img.get('data-image-name')
                    if imgsrc == None:
                        imgsrc = div2.a.img.get('src')
                    downimg(imgsrc, 'static/fbimg/' + dataimagename)
                    sectionobj["stages"].append(
                        {"title": title, "img": dataimagename})
                    if not os.path.exists('static/stages/' + title + '.json'):
                        gettask(
                            {"title": title, "img": dataimagename, "type": "旅人的記憶"})
    fw = open('static/xuying2.json', 'w', encoding='utf-8')
    model = json.dumps(d, ensure_ascii=False, indent=2)
    fw.write(model)
    fw.close()


def getxuying(allupdate):
    n = quote("虛影世界")
    download_url = "https://tos.fandom.com/zh/wiki/Template:" + n + "?action=edit"
    soup = downlink(download_url)
    if soup == None:
        return
    textarea = soup.findAll('textarea')[0].string
    # f =open('1.html', encoding='utf-8')
    # textarea=f.read()
    textarea = textarea.replace(
        '===機械城之傳===', "<center>'''機械城之傳'''</center>").replace('{{!}}-{{!}}', "")
    sections = re.search(
        r"<div class=\"rstage\".*>{{#tag:tabber\|([\s\S]+?)}}\<\/div\>", textarea)
    d = re.sub(r'([^\s]*)=', r'# \1', sections.group(1))
    d = re.sub(r"<center>'''([^']*)'''</center>", r'### \1', d)
    d = re.sub(r"'''([^']*)'''", r'\1', d)
    stagegroup = re.split(r"{{DIcon\|[^\|]*\|([^\|]*).*", d)
    xuyingstages = []
    for i in range(1, len(stagegroup), 2):
        stagename = str.strip(stagegroup[i])
        xuyingstages.append(stagename)
        fb = {'title': stagename, 'type': '虛影世界'}
        if not os.path.exists('static/stages/' + stagename + '.json') or allupdate:
            gettask(fb)
    d = re.sub(r"{{DIcon\|([^\|]*)\|([^\|]*).*",
               r'![\2](fbimg/\1i.png) [\2](\2)', d)
    dd = ""
    dg = []
    for ll in d.splitlines():
        ll = str.strip(ll)
        if ll == '':
            continue
        if ll[0] == "!":
            va = re.split("(\(.+?\))", ll)
            va[len(va) - 2] = "(/pages/index/detail/detail?name=" + \
                urllib.parse.quote(va[len(va) - 2][1:-1]) + ")"
            ll = "".join(va)
        dd += ll + "\n"
        if ll[0] == '#' and ll[1] == ' ':
            o = {"title": ll[2:], "data": ""}
            if dd != '':
                dg.append(o)
        o["data"] += ll + "\n"
    for dggg in dg:
        dggg["data"] = "\n".join(dggg["data"].split("\n")[1:])
    fw = open('static/xuying.json', 'w', encoding='utf-8')
    fw.write(json.dumps(dg, ensure_ascii=False, indent=2))
    fw.close()
    fw = open('static/xuyingstages.json', 'w', encoding='utf-8')
    fw.write(json.dumps(xuyingstages, ensure_ascii=False, indent=2))
    fw.close()


def gettosmonster():
    # f1 = open('main.19ec43eb.chunk.js', encoding='utf-8')
    # jsstr = f1.read()
    href = "https://gallery.tosgame.com/#/filter"
    soup = downlink(href)
    if soup == None:
        return
    jsstr = ""
    for sc in soup.findAll('script'):
        scsrc = sc.get('src')
        if scsrc and scsrc.startswith("./static/js/main"):
            href = "https://gallery.tosgame.com/" + scsrc[2:]
            jsstr = downurl(href)
    r = re.match(r'[\s\S]*Y=(\[[\s\S]*\]),V=', jsstr)
    if r:
        Y = r.groups()[0]
        ctx = execjs.compile("function get() {return " + Y + "}")
        gjson_obj = ctx.call("get")

    r = re.match(r'[\s\S]*dt=(\[[\s\S]*\]),mt=', jsstr)
    if r:
        Y = r.groups()[0]
        ctx = execjs.compile("function get() {return " + Y + "}")
        json_obj = ctx.call("get")

        newjsob = []
        tj = {"tag": []}
        for item in json_obj:
            for g in gjson_obj:
                if g["id"] == item["groupId"]:
                    newjsob.append({"id": "%03d" % item["id"], "name": item["name"], "rare": str(item["star"]), "attr": getattr(
                        item["attribute"]), "race": getrace(
                        item["race"]), "series": g["name"], "tags": item["types"]})
                    for tag in item["types"]:
                        if tag not in tj["tag"]:
                            tj["tag"].append(tag)
        fw = open('static/monster_JSON.json', 'w', encoding='utf-8')
        fw.write(json.dumps(newjsob, ensure_ascii=False, indent=2))
        fw.close()

        zhsseries = []
        for g in gjson_obj:
            if g["total"] >= 5:
                zhsseries.append(g["name"])
        fw = open('static/zhsseries.json', 'w', encoding='utf-8')
        model = json.dumps(zhsseries, ensure_ascii=False, indent=2)
        fw.write(model)
        fw.close()

        fw = open('static/zhstj.json', 'w', encoding='utf-8')
        model = json.dumps(tj, ensure_ascii=False, indent=2)
        fw.write(model)
        fw.close()


def getattr(attribute):
    if attribute == 1:
        return "水"
    if attribute == 2:
        return "火"
    if attribute == 3:
        return "木"
    if attribute == 4:
        return "光"
    if attribute == 5:
        return "暗"
    return str(attribute)


def getrace(race):
    if race == 1:  # confirm
        return "人類"
    if race == 2:
        return "獸類"
    if race == 3:
        return "妖精類"
    if race == 4:
        return "龍類"
    if race == 5:
        return "神族"
    if race == 8:
        return "魔族"
    if race == 10:  # confirm
        return "機械族"
    if race == 6:
        return "素材"
    return str(race)


if __name__ == "__main__":
    if not os.path.exists('static'):
        os.mkdir('static')
    if not os.path.exists('static/bg'):
        os.mkdir('static/bg')
    if not os.path.exists('static/toswikiapic'):
        os.mkdir('static/toswikiapic')
    if not os.path.exists('static/stages'):
        os.mkdir('static/stages')
    if not os.path.exists('static'):
        os.mkdir('static')
    if not os.path.exists('static/zhs'):
        os.mkdir('static/zhs')
    if not os.path.exists('static/es'):
        os.mkdir('static/es')
    if not os.path.exists('static/common'):
        os.mkdir('static/common')
    if not os.path.exists('static/lk'):
        os.mkdir('static/lk')
    if not os.path.exists('static/skill'):
        os.mkdir('static/skill')
    if not os.path.exists('static/fbimg'):
        os.mkdir('static/fbimg')
    if not os.path.exists('static/tags'):
        os.mkdir('static/tags')
    if not os.path.exists('static/ver.json'):
        fw = open('static/ver.json', 'w', encoding='utf-8')
        fw.write('{}')
        fw.close()
    # 最近关卡，及副本图片
    # mfs = 'https://static.wikia.nocookie.net/tos/images/a/ab/Gift-%E9%AD%94%E6%B3%95%E7%9F%B3.png/revision/latest/scale-to-width-down/40?cb=20171216040121&path-prefix=zh'
    # downimg(mfs, 'static/toswikiapic/Gift-mfs.png')
    # lh = 'https://static.wikia.nocookie.net/tos/images/d/d4/Gift-%E9%9D%88%E9%AD%82.png/revision/latest/scale-to-width-down/40?cb=20200512084425&path-prefix=zh'
    # downimg(lh, 'static/toswikiapic/Gift-lh.png')
    # skill1 = 'https://static.wikia.nocookie.net/tos/images/5/58/Skill1.png/revision/latest/scale-to-width-down/50?cb=20150131155718&path-prefix=zh'
    # downimg(skill1, 'static/toswikiapic/skill1.png')
    # skill2 = 'https://static.wikia.nocookie.net/tos/images/4/4c/Skill2.png/revision/latest/scale-to-width-down/50?cb=20150131155718&path-prefix=zh'
    # downimg(skill2, 'static/toswikiapic/skill2.png')
    # skill3 = 'https://static.wikia.nocookie.net/tos/images/f/f7/Skill3.png/revision/latest/scale-to-width-down/50?cb=20150131155718&path-prefix=zh'
    # downimg(skill3, 'static/toswikiapic/skill3.png')
    # yaoshi = 'https://static.wikia.nocookie.net/tos/images/3/3e/Item13.png/revision/latest/scale-to-width-down/30?cb=20160112111448&path-prefix=zh'
    # downimg(yaoshi, 'static/toswikiapic/yaoshi.png')
    # jinbi = 'https://static.wikia.nocookie.net/tos/images/0/0b/ICON076.png/revision/latest/scale-to-width-down/30?cb=20130614092534&path-prefix=zh'
    # downimg(jinbi, 'static/toswikiapic/jinbi.png')
    # tili = 'https://static.wikia.nocookie.net/tos/images/c/c4/Gift-%E9%AB%94%E5%8A%9B.png/revision/latest/scale-to-width-down/30?cb=20180623122951&path-prefix=zh'
    # downimg(tili, 'static/toswikiapic/tili.png')
    # zlys = 'https://static.wikia.nocookie.net/tos/images/5/5d/Gift-%E6%88%B0%E9%9D%88%E8%97%A5%E6%B0%B4.png/revision/latest/scale-to-width-down/40?cb=20200420001411&path-prefix=zh'
    # downimg(zlys, 'static/toswikiapic/zlys.png')
    # exp= 'https://static.wikia.nocookie.net/tos/images/9/9c/Exp.png/revision/latest/scale-to-width-down/25?cb=20130209054852&path-prefix=zh'
    # downimg(exp, 'static/toswikiapic/exp.png')
    # huihe = 'https://static.wikia.nocookie.net/tos/images/7/70/Battle.png/revision/latest/scale-to-width-down/24?cb=20130209054844&path-prefix=zh'
    # downimg(huihe, 'static/toswikiapic/huihe.png')
    # tili2 = 'https://static.wikia.nocookie.net/tos/images/8/8d/Stamina.png/revision/latest/scale-to-width-down/25?cb=20130924035103&path-prefix=zh'
    # downimg(tili2, 'static/toswikiapic/tili2.png')

    # print(datetime.date.today()+datetime.timedelta(days=1))
    # getrecent()
    # getrecenttask()
    # getrecentimg()

    # 主线
    # getmainline(False)
    # getmainlineimg(quote("主線任務#.E7.AC.AC1-6.E5.B0.81.E5.8D.B0") + "")

    # 虚影
    # getxuying(True)
    # getmainlineimg(quote("虛影世界"))

    # 旅人的记忆
    # getlvren() # 过时
    # getlvrenbyapi(True)

    # 获取场景特性

    # 召唤兽
    obj = TestClass()
    # obj.getallzhs('1-300')
    # obj.getallzhs('301-600')
    # obj.getallzhs('601-900')
    # obj.getallzhs('901-1200')
    # obj.getallzhs('1201-1500')
    # obj.getallzhs('1501-1800')
    # obj.getallzhs('1801-2100')
    # obj.getallzhs('2101-2400')
    # obj.getallzhs('2401-2700')
    # obj.getallzhs('其它A-Z')
    obj.mergeallzhs()  # 将所有资料合并到zhsseries.json

    # d = ["2", "23", "123"]
    # print("1" in d)
    # getzhs("2534")
    # getskill("給我一雙翅膀", None)

    # 龙刻
    # getalllk()
    # getalllkimg()

    # 召唤兽
    # gettosmonster()

    # getfbimg("虛影世界") # 旅人的记忆 虛影世界 主線任務
    # 803 "黃金之日", "魔法閣的邀請", "來自西域的雙頭龍", "結伴飛翔的兄弟", "以創作起革命", "妖精翩翩起舞"
    # "美麗的炸藥", "一路向前的象", "惡戲破壞", "無名的熊孩子", "掙扎求生的本能", "不可輕敵"
    # "愛的抱抱", "即使世界崩塌"
    # "甦醒的過去", "不擇手段地搶奪", "魔族的威脅"
    # for s in ["1"]:  # 歡樂的包容者, 背叛北域的人,通過畢業考試 (上), 粉碎重生者的憎恨, 累積的憎恨
    #     gettask({
    #             "title": s,  # 無名的熊孩子  掙扎求生的本能 不可輕敵  魔法閣的邀請
    #             "type": "地獄級關卡",  # 旅人的記憶, 虛影世界,地獄級關卡
    #             "img": "static/zhs/086i.png"
    #             })

    # 主线更新
    # - static/mainline.txt
