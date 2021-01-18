# coding=utf-8
import requests
from lxml import etree
from requests.exceptions import ConnectionError


"""
爬虫api：
    搜索结果页：get_index_result(search)
    小说章节页：get_chapter(url)
    章节内容：get_article(url)
"""


class DdSpider(object):

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
        }

    def parse_url(self, url):
        try:
            resp = requests.get(url, headers=self.headers)
            if resp.status_code == 200:
                # 处理一下网站打印出来中文乱码的问题
                resp.encoding = 'utf-8'
                return resp.text
            return None
        except ConnectionError:
            print('Error.')
        return None

    # 搜索结果页数据
    def get_index_result(self, search, page=0):
        if page == 0:
            url = 'http://zhannei.baidu.com/cse/search?s=1682272515249779940&entry=1&q={search}'.format(
                search=search)
        else:
            url = 'http://zhannei.baidu.com/cse/search?q={search}&p={page}&s=1682272515249779940'.format(
                search=search, page=page)
        resp = self.parse_url(url)
        html = etree.HTML(resp)
        titles = html.xpath('//*[@id="results"]/div/div/div/h3/a/@title')
        urls = html.xpath('//*[@id="results"]/div/div/div/h3/a/@href')
        images = html.xpath('//*[@id="results"]/div/div/div/a/img/@src')
        authors = html.xpath(
            '//*[@id="results"]/div/div/div/div/p[1]/span[2]/text()')
        profiles = html.xpath('//*[@id="results"]/div/div/div/p/text()')
        styles = html.xpath(
            '//*[@id="results"]/div/div/div/div/p[2]/span[2]/text()')
        times = html.xpath(
            '//*[@id="results"]/div/div/div/div/p[3]/span[2]/text()')
        print(titles)
        for title, url, image, author, profile, style, tim in zip(titles, urls, images, authors, profiles, styles,
                                                                  times):
            data = {
                'title': title.strip(),
                'url': url,
                'image': image,
                'author': author.strip(),
                'profile': profile.strip().replace('\u3000', '').replace('\n', ''),
                'style': style.strip(),
                'time': tim.strip()
            }
            yield data

    # 小说章节页数据
    def get_chapter(self, url):
        resp = self.parse_url(url)
        html = etree.HTML(resp)
        chapters = html.xpath('//*[@id="main"]/div/dl/dd/a/text()')
        urls = html.xpath('//*[@id="main"]/div/dl/dd/a/@href')
        for chapter_url, chapter in zip(urls, chapters):
            data = {
                'url': str(url) + chapter_url,
                'chapter': chapter
            }
            yield data

    # 章节内容页数据
    def get_article(self, url):
        resp = self.parse_url(url)
        html = etree.HTML(resp)
        content = html.xpath('//div[@class="read_list"]/a')
        # print(content.text)
        titles=[]
        for i in content:
            # print(i.tag)  # script 标签名
            # document.getElementById('video_iframe').src="https://video.vdonghua.cn/player/833cd31f7d2641fabd788007f170daa8?r="+(new Date()).getTime(); 文本内容
            print(i.text)
            print(i.attrib["href"])
            titles.append(i.text)
            continue
            print(i.attrib)  # {'type': 'text/javascript'} 标签中属性
            for x in i.attrib:
                if x == 'type':
                    # 通过属性的key获得对应的value
                    print(i.attrib.get(x))  # text/javascript
                    print(i.attrib.get('type'))  # text/javascript
            # 属性名称的迭代传递
            for x in i.attrib.iterkeys():
                print(x)  # type 属性的key
                print(type(x))  # <type 'str'>

            # 属性值的迭代传递
            for x in i.attrib.itervalues():
                print(x)  # type 属性的key
                print(type(x))  # <type 'str'>

            # 属性的迭代传递
            for x in i.attrib.iteritems():
                print(x)  # type 属性的key
                print(type(x))  # <type 'str'>
        return '<br>'.join(titles)


dd = DdSpider()
# for i in dd.get_index_result('诛仙',page=0):
#     print(i)
print(dd.get_article('https://www.txt909.com/readbook/3571.html'))
