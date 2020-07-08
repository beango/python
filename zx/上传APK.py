#! python2
# encoding: utf-8
# client.py

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2

#python2 -m pip install poster
url = "http://localhost:8080/uploadAPK"
upload_file_path = "/work/workspace/python/zx/1.jpg"
filename = "1-1.jpg"

if __name__ == '__main__':
    register_openers()
    datagen, headers = multipart_encode({"file": open(upload_file_path, "rb")
        ,"type":"uploadFile","fileName":filename,"prdcode":"ZX-AP10Inch-YS","apkver":"ZX-AP10Inch-YS-1.3.0.apk", "userid":"4028818A6F45743F016F45743FC80000"})
    request = urllib2.Request(url, datagen, headers)
    response = urllib2.urlopen(request).read()
    print(response)