# encoding: UTF-8
import re

file_object = open('u_ex141222.log')
list_of_all_the_lines = file_object.readlines()
pattern = re.compile(r'(.*)(/Report/RecordCheckByCustomer.aspx customerid=[0-9]*)')
pattern1 = re.compile(r'(.*)(/Report/RecordCheckbyCustomer.aspx page=[0-9]*&stime=[0-9,-]*&etime=[0-9,-]*&customerid=[0-9]*&eid=[0-9]*)(.*)')

for line in list_of_all_the_lines:
	match = pattern.split(line)
	if len(match)>1:
		print match[2]

	match1 = pattern1.split(line)
	if len(match1)>1:
		print match1[2]


'''
pattern1 = re.compile(r'(.*)(/Report/RecordCheckbyCustomer.aspx page=[0-9]*&stime=[0-9,-]*&etime=[0-9,-]*&customerid=[0-9]*&eid=[0-9]*)(.*)')
match1 = pattern1.split('2014-12-22 01:14:54 192.168.1.86 GET /Report/RecordCheckbyCustomer.aspx page=0&stime=2014-12-12&etime=2014-12-19&customerid=201411272320007619&eid=11 6666 - 192.168.0.1 Mozilla/4.0+(compatible;+MSIE+8.0;+Windows+NT+5.1;+Trident/4.0;+.NET+CLR+2.0.50727;+.NET+CLR+3.0.04506.648;+.NET+CLR+3.5.21022) 200 0 0 1482')
if len(match1)>1:
	print match1[2]
'''
