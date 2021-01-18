#!/usr/bin/python
# -*- coding: utf-8 -*-  

from bs4 import BeautifulSoup
from urllib.request import urlopen

content = ""
file_object = open('/home/beango/Pictures/1.html')
try: 
    for line in file_object:
         content += line
finally:
     file_object.close()

#html = urlopen("/home/beango/Pictures/1.html").read().decode('utf-8')

soup = BeautifulSoup(content, features='lxml')
tables = soup.find_all("table",{"class","wikitable"})
for table in tables:
  
  trs = table.findChildren('tr')    
  for tr in trs:        
      tline = ""
      td = tr.findChildren('td')
      if len(td) > 0:
        tline += str.strip(td[0].text)
      if len(td) > 1:
        tline += u", " + str.strip(td[1].text)
      if len(td) > 2:
        spans = td[2].findChildren("span")
        aarr = spans[0].findChildren("a")
        if len(aarr) > 1:
          tline += u", " + aarr[1].text
        [s.extract() for s in td[2]('span')]
        tline += "(" + str.strip(td[2].text) + ")"
      print(tline)
  