# -*- coding:utf8 -*-
# 2014.1.28 14:13 为贴吧签到0.1编写保存帐号信息的脚本

import os
import pickle

def account():
	#检测txt是否存在，不存在则创建包含空字典的txt
	if not os.path.exists('config.txt'):
		print u'初始化用户配置'
		account = {}
		f1 = open('config.txt','wb')
		pickle.dump(account,f1)
		f1.close()

	# load 字典
	f2 = open('config.txt','rb')
	account = pickle.load(f2)
	f2.close()

	if account !={}:
		print u'以下是已保存的用户帐号：'
		for key in account.keys():
			print key.decode('gbk')
		print u'请输入数字来选择对应的帐号。如果您要填写新的帐号，直接按回车键'
		num = raw_input('>')
		##############################可以是原来帐号，也可以是现在的帐号
		try:
			id = account.items()[int(num)-1]
			#print id    这是什么编码？('\xb0\xd9\xca\xc2\xb2\xbb\xca\xc7\xb6\xab\xce\xf7', '*********') 
			(name,pwd)=id

		except:	
			name = raw_input(u'请输入用户名，按回车键结束:'.encode('gbk'))
			pwd = raw_input(u'请输入密码:，按回车键结束:'.encode('gbk'))
			#写入字典

			account[name] = pwd
			f3 = open('config.txt','wb')
			pickle.dump(account,f3)
			f3.close()
	else:
		name = raw_input(u'请输入用户名，按回车键结束:'.encode('gbk'))
		pwd = raw_input(u'请输入密码:，按回车键结束:'.encode('gbk'))
		#写入字典

		account[name] = pwd
		f3 = open('config.txt','wb')
		pickle.dump(account,f3)
		f3.close()
	print name,pwd
	return (name,pwd)