import requests
import lxml.etree
import json, os

start_url = "http://www.quanshuwang.com/"

response = requests.get(start_url)
response.encoding = "gbk"
# print(response.text)

html = lxml.etree.HTML(response.text)

categorys = html.xpath("//ul[@class='channel-nav-list']/li/a")

categories = []
if os.path.exists('../static/categories.json'):
    f = open('../static/categories.json', encoding='utf-8')
    res = f.read()
    if res != "":
        categories = json.loads(res)


for category in categorys:
    url = category.xpath("./@href")[0]
    name = category.xpath("./text()")[0]
    print(name,":",url)
    print("----------------------------------------")
    if name not in categories:
        categories.append({"name": name, "books": []})
fw = open('../static/categories.json', 'w', encoding='utf-8')
json.dump(categories, fw, ensure_ascii=False, indent=2)
fw.close()
