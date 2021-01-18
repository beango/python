import requests
import lxml.etree
import json, os
import urllib

start_url = "http://www.quanshuwang.com/"

response = requests.get(start_url)
response.encoding = "gbk"
# print(response.text)

html = lxml.etree.HTML(response.text)

categorys = html.xpath("//ul[@class='channel-nav-list']/li/a")

categories = {}
if os.path.exists('../static/categories.json'):
    f = open('../static/categories.json', encoding='utf-8')
    res = f.read()
    if res != "":
        categories = json.loads(res)


for category in categorys:
    books=[]
    cateurl = category.xpath("./@href")[0]
    name = category.xpath("./text()")[0]
    print(name,":", cateurl)
    print("----------------------------------------")
    if name not in categories:
        categories[name] = books
    else:
        books = categories[name]
        
    response_1 = requests.get(cateurl)
    response_1.encoding = "gbk"
    
    html_1 = lxml.etree.HTML(response_1.text)
    urls = html_1.xpath("//ul[@class='seeWell cf']/li/span/a[1]/@href")
    for url in urls:
        response_2 = requests.get(url)
        response_2.encoding = "gbk"
        html_2 = lxml.etree.HTML(response_2.text)
        title = html_2.xpath("//div[@class='b-info']/h1/text()")[0]
        trueUrl = html_2.xpath("//div[@class='b-oper']/a[@class='reader']/@href")[0]
        author = html_2.xpath("//div[@class='bookDetail']/dl[@class='bookso']/dd[1]/text()")[0].strip()
        intro = html_2.xpath("//div[@id='waa']/text()")[0].strip()
        imgUrl = html_2.xpath("//a[@class='l mr11']/img/@src")[0]

        filename = title + '.jpg'
        dirpath = '../static/cover'
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        filepath = os.path.join(dirpath,filename)
        try:
            urllib.request.urlretrieve(imgUrl, filepath)
        except Exception as e:
            print("imgUrl", imgUrl, e)

        cover = 'cover/' + filename
        if title not in books:
            books.append({"title": title, "author": author, "cover":cover, "intro": intro})
        print(title,":",trueUrl,author,'\n',intro,cover)
        print("-----------------------------------------------")


fw = open('../static/categories.json', 'w', encoding='utf-8')
json.dump(categories, fw, ensure_ascii=False, indent=2)
fw.close()
