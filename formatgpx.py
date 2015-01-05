#!/usr/bin/env python
# -*- coding: utf-8 -*-
# chatserv.py
#
# sockchat serv
from xml.etree.ElementTree import ElementTree,Element  
  
def read_xml(in_path):  
    '''''读取并解析xml文件 
       in_path: xml路径 
       return: ElementTree'''  
    tree = ElementTree()  
    tree.parse(in_path)  
    return tree  
  
def write_xml(tree, out_path):  
    '''''将xml文件写出 
       tree: xml树 
       out_path: 写出路径'''  
    tree.write(out_path, encoding="utf-8",xml_declaration=True)  
  
def if_match(node, kv_map):  
    '''''判断某个节点是否包含所有传入参数属性 
       node: 节点 
       kv_map: 属性及属性值组成的map'''  
    for key in kv_map:  
        if node.get(key) != kv_map.get(key):  
            return False  
    return True  
  
#---------------search -----  
  
def find_nodes(tree, path):  
    '''''查找某个路径匹配的所有节点 
       tree: xml树 
       path: 节点路径'''  
    return tree.findall(path)  
  
  
def get_node_by_keyvalue(nodelist, kv_map):  
    '''''根据属性及属性值定位符合的节点，返回节点 
       nodelist: 节点列表 
       kv_map: 匹配属性及属性值map'''  
    result_nodes = []  
    for node in nodelist:  
        if if_match(node, kv_map):  
            result_nodes.append(node)  
    return result_nodes  
  
#---------------change -----  
  
def change_node_properties(nodelist, kv_map, is_delete=False):  
    '''''修改/增加 /删除 节点的属性及属性值 
       nodelist: 节点列表 
       kv_map:属性及属性值map'''  
    for node in nodelist:  
        for key in kv_map:  
            if is_delete:   
                if key in node.attrib:  
                    del node.attrib[key]  
            else:  
                node.set(key, kv_map.get(key))  
              
def change_node_text(node, text, is_add=False, is_delete=False):  
    '''''改变/增加/删除一个节点的文本 
       nodelist:节点列表 
       text : 更新后的文本'''  
    if is_add:  
		node.text += text  
    elif is_delete:  
		node.text = ""  
    else:  
		node.text = text  
              
def create_node(tag, property_map, content):  
    '''''新造一个节点 
       tag:节点标签 
       property_map:属性及属性值map 
       content: 节点闭合标签里的文本内容 
       return 新节点'''  
    element = Element(tag, property_map)  
    element.text = content  
    return element  
          
def add_child_node(nodelist, element):  
    '''''给一个节点添加子节点 
       nodelist: 节点列表 
       element: 子节点'''  
    for node in nodelist:  
        node.append(element)  
          
def del_node_by_tagkeyvalue(nodelist, tag, kv_map):  
    '''''同过属性及属性值定位一个节点，并删除之 
       nodelist: 父节点列表 
       tag:子节点标签 
       kv_map: 属性及属性值列表'''  
    for parent_node in nodelist:  
        children = parent_node.getchildren()  
        for child in children:  
            if child.tag == tag and if_match(child, kv_map):  
                parent_node.remove(child)  

#xmlns="http://www.topografix.com/GPX/1/1"
import time,datetime
sfile = '2014-09-09 19_53.gpx'
s = sfile.replace('.gpx','').replace('_',':')+':00'
tfile = '2014-09-10 20_04.gpx'
t = tfile.replace('.gpx','').replace('_',':')+':00'

s1 = datetime.datetime(int(s[0:4]),int(s[5:7]),int(s[8:10]),int(s[11:13]),int(s[14:16]),int(s[17:19]))
t1 = datetime.datetime(int(t[0:4]),int(t[5:7]),int(t[8:10]),int(t[11:13]),int(t[14:16]),int(t[17:19]))
inte = (t1-s1).seconds

gpx = read_xml(r'./'+sfile)
timelist = find_nodes(gpx,"trk/trkseg/trkpt/time")
for timenod in timelist:
	curt = timenod.text
	curtime = timenod.text.replace('T',' ').replace('Z',' ')[0:19]
	curtime1 = time.strptime(curtime,'%Y-%m-%d %H:%M:%S')
	Y,m,d,H,M,S = curtime1[0:6]
	strtime = str(datetime.datetime(Y,m,d,H,M,S)+datetime.timedelta(seconds=inte))
	newt = t[0:10]+'T'+strtime[11:19]+'.'+curt[20:]

	#print timenod.text
	change_node_text(timenod,newt)

	#print timenod.text

write_xml(gpx, "./"+tfile)
