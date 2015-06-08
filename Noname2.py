# encoding: UTF-8
import re

file_object = open('t1/20150511.log')
list_of_all_the_lines = file_object.readlines()
pattern = re.compile(r'(.*)(http://192.168.1.118:808/Csvr/Call/CallLog?)')

for line in list_of_all_the_lines:
	match = pattern.split(line)
	if len(match)>1:
		print 'http://192.168.1.118:808/Csvr/Call/CallLog'+match[3]