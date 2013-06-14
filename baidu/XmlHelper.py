#-*- coding: UTF-8 -*-
#!/usr/bin/env python  
#coding:utf-8  

from  xml.dom import  minidom
import sys,json,re
from xml.sax.saxutils import unescape
reload(sys)
sys.setdefaultencoding('utf-8')

def get_attrvalue(node, attrname):
     return node.getAttribute(attrname) if node else ''

def get_nodevalue(node, index = 0):
    #print node.childNodes[1].nodeValue
    #return node.childNodes[index].nodeValue if node else ''
    return "".join([n.nodeValue for n in node.childNodes if n])

def get_xmlnode(node,name):
    return node.getElementsByTagName(name) if node else []

def xml_to_string(filename='1.xml'):
    doc = minidom.parse(filename)
    return doc.toxml('UTF-8')

def get_xml_plant(filename='1.xml'):
    doc = minidom.parse(filename) 
    root = doc.documentElement
    crops = get_xmlnode(root,'crops')

    objs = json.loads(get_nodevalue(crops[0]))
    print len([i for i in objs["crops"] if "成熟" in i["nextText"]])
    print len([i for i in objs["crops"] if "盛开" in i["nextText"]])
    print len([i for i in objs["crops"] if "成苗" in i["nextText"]])
    print len([i for i in objs["crops"] if "结果" in i["nextText"]])

    print ([i["id"] for i in objs["crops"] if re.split(",",i["nextText"])[-1:][0] not in["成熟","盛开","成苗","结果"]])
    print len(objs["crops"])

    return objs["crops"]

if __name__ == "__main__":
    get_xml_plant(filename='Data/frame_data.xml')