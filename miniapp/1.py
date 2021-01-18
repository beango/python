# -*- coding:UTF-8 -*-
from urllib import request
from bs4 import BeautifulSoup
import json, time, os, socket
timeout = 2
socket.setdefaulttimeout(timeout)

download_url = "https://www.tosapp.tw" #tosapp.html
head = {}
head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
download_req = request.Request(url = download_url, headers = head)
download_response = request.urlopen(download_req)
download_html = download_response.read().decode('utf-8','ignore')
soup = BeautifulSoup(download_html, 'lxml')
# print(soup_texts)
# soup = BeautifulSoup(open('c:/workspace/python/tosapp.html', "r", encoding='utf-8'),'lxml')
daily=soup.select('div .daily')
d = []
if not os.path.exists('cardpic'):
    os.mkdir('cardpic')
for dailybox in daily[0].select('div .daily_box'):
    img_src = (dailybox.select('div .daily_cont >img')[0].get("src"))
    d.append({'title': dailybox.select('div .daily_cont >div >a')[0].get_text(),
             'type': dailybox.select('div .daily_cont >div >font')[0].get_text(),
             'img': img_src,
             'date': dailybox.select('div .daily_header > p')[0].get_text()})
    img_url = download_url + "/" + img_src
    print(img_url)
    request.urlretrieve(img_url, img_src) 
fw =open('daily.json','w',encoding='utf-8')
d.append({'updatetime': time.time()})
json.dump(d, fw, ensure_ascii=False,indent=2)