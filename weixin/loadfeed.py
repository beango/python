#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import urllib
from xml.dom import minidom

class loadfeed:
    def get_xmlnode(self, node,name):
        return node.getElementsByTagName(name) if node else []

    def get_attrvalue(self, node, attrname):
         return node.getAttribute(attrname) if node else ''

    def get_nodevalue(self, node, index = 0):
        if node.childNodes.length==0 :
            return ''
        return node.childNodes[index].nodeValue if node else ''

    def get_xml_data(self, filename):
        doc = minidom.parse(filename) 
        root = doc.documentElement

        item_nodes = self.get_xmlnode(root,'item')
        arr_list=[]
        for item in item_nodes: 
            title = self.get_xmlnode(item,'title') 
            link = self.get_xmlnode(item,'link') 
            img = self.get_xmlnode(item,'img')
            arr = {}
            arr['title'] , arr['link'], arr['images'] = (
                self.get_nodevalue(title[0]).encode('utf-8','ignore'), 
                self.get_nodevalue(link[0]),
                self.get_nodevalue(img[0])
            )
            arr_list.append(arr)
        return arr_list

    def getfeed(self, fileurl):
        urllib.urlretrieve(fileurl, "log/feed.xml")
        return self.get_xml_data("log/feed.xml")
