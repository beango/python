#!/usr/bin/python
#coding=utf-8
 
import urllib,urllib2
import random 
import time
import datetime

uri = 'http://192.168.1.199:8080/appriesAddSpByPantryn'
idcard = ['0000','1','1007','1047','1048','1050','1052','1054','1055','1056','10565','1057','1058','1059','1060','1063','1064','1065','1067','1068','1069','1071','1072','1073','1074','1077','1078','1080','1082','1083','1084','1085','1086','1087','1088','1092','1093','1094','1096','1101','1102','1103','1105','1106','1107','111','1111','1113','1114','1116','1117','1120','1123','1124','1125','1126','1132','1133','1134','1139','1141','1146','11496','1153','1156','1160','1161','1163','1164','1166','1168','1174','1175','1183','1185','1191','1192','1193','1196','1202','1203','1204','1206','1207','1209','1210','1211','1212','1214','1216','1217','1218','1220','1225','1226','1227','1228','1229','1230','1231']
mac = ['1','10','10D07AEA2A44','11','12','13','14','15','16','17','18','19','2','20','21','22','2323','3','4','5','6','7','8','9']

i = 1
count = 298
t = datetime.datetime.strptime("2019-05-17 8:36:00", "%Y-%m-%d %H:%M:%S")
while i<=count:
	r = random.randint(100, 170)
	t = t + datetime.timedelta(seconds = r)
	print r, t
	params = {};
	params['tt'] = t.strftime("%Y-%m-%d %H:%M:%S")
	params['mac'] = mac[random.randint(0, len(mac)-1)]
	params['cardnum'] = idcard[random.randint(0, len(idcard)-1)]
	params['pj'] = random.randint(0, 3)
	params['idcard'] = ''
	params['ywlsh'] = ''
	params = urllib.urlencode(params)
	req = urllib2.Request(uri, params) 
	response = urllib2.urlopen(req) 
	i+=1



