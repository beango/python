#!/usr/bin/env python
# -*- coding: utf-8 -*-

from spyne import ServiceBase, Iterable, Unicode, Integer, Application, rpc
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import yaml
import os
import json
import xmltodict
import sys,time,random,types,socket

def get_yaml_data(yaml_file):
    # 打开yaml文件
    print("***获取yaml文件数据***")
    file = open(yaml_file, 'r')
    file_data = file.read()
    file.close()
    
    print(file_data)
    print("类型：", type(file_data))

    # 将字符串转化为字典或列表
    print("***转化yaml数据为字典或列表***")
    data = yaml.load(file_data)
    print(data)
    print("类型：", type(data))
    return data

def xmltojson(xmlstr):
    #parse是的xml解析器
    xmlparse = xmltodict.parse(xmlstr)
    #json库dumps()是将dict转化成json格式，loads()是将json转化成dict格式。
    #dumps()方法的ident=1，格式化json
    jsonstr = json.dumps(xmlparse, indent=1)
    jsondata = json.loads(jsonstr)
    return jsondata

class Call(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def sendUDP(self, send_data):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dest_addr = ('192.168.5.136', 9002)  # 注意 是元组，ip是字符串，端口是数字
        udp_socket.sendto(send_data.encode('gb2312'), dest_addr)
        udp_socket.close()

    def Call(self, Call_PatientInfo):
        patient_info = xmltojson(Call_PatientInfo)
        print('call_room:', patient_info["patient_info"]['call_room'])
        pat_name = 'call_room:', patient_info["patient_info"]['pat_name']
        #self.sendUDP(pat_name)
        return "Call Success"
 
application = Application([Call],
                          tns='spyne.examples.call',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    current_path = os.path.abspath(".")
    yaml_path = os.path.join(current_path, "config.yaml")
    config = get_yaml_data(yaml_path)
    print(config["CallStation_1"]['CallStationip'])
    port = config["config"]['port']
    
    wsgi_app = WsgiApplication(application)
    server = make_server('0.0.0.0', port, wsgi_app)
    server.serve_forever()