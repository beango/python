from zeep import Client

client = Client('http://www.webxml.com.cn/WebServices/WeatherWS.asmx?WSDL')
#print(client.service.getRegionCountry())



client = Client('http://www.dneonline.com/calculator.asmx?WSDL')
#print(client.service.Add(1,2))

# 47.107.110.82
client = Client('http://47.107.110.82:8089/ws/ad.wsdl')
xml ="<patient_info><call_area>皮肤科分诊区</call_area><call_room>皮肤科门诊三诊室</call_room><IPaddress>172.16.16.70</IPaddress><doctor_title></doctor_title><doctor_call_name>冯跃碧</doctor_call_name><doctor_id>0010920</doctor_id><doctor_profile></doctor_profile><call_no>21</call_no><pat_name>赵谊</pat_name><wait_call_no1>16</wait_call_no1><wait_pat_name1>陈奕霖</wait_pat_name1><wait_call_no2></wait_call_no2><wait_pat_name2></wait_pat_name2><call_kind>普通</call_kind></patient_info>"
print(client.service.Call(xml))