from scrapy import cmdline
import os

if not os.path.exists('../static'):
    os.makedirs('../static')
if not os.path.exists('../static/cover'):
    os.makedirs('../static/cover')

cmdline.execute('scrapy crawl quanshuwang'.split())

# spider = QuanshuwangSpider()
# start_url = "http://www.quanshuwang.com/"

# response = requests.get(start_url)
# response.encoding = "gbk"
# # print(response.text)
# html = lxml.etree.HTML(response.text)

# tt = spider.parse(html)
# for b in tt:
#     print(b.text)
