#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui , QtCore

class MainWindow(QtGui.QWidget):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__()

		#QtGui.QWidget.__init__(self, parent)
		self.resize( 300 , 250 )
		self.setWindowTitle(u'窗口标题')

		# 设置图标
		self.setWindowIcon(QtGui.QIcon(u'16-111129230521'))

		# 设置窗口中间部分的文字tip提示
		self.setToolTip('This is a <b>QWidget</b> widget')
		QtGui.QToolTip.setFont(QtGui.QFont('OldEnglish', 12))

		# 退出按钮
		quit = QtGui.QPushButton(u'退出', self)
		quit.setGeometry(10, 20, 50, 30)

		# 退出按钮 连接 到py的信号槽机制
		self.connect(quit, QtCore.SIGNAL('clicked()'), QtGui.qApp, QtCore.SLOT('quit()'))
		self.center();
		
	def center(self):
	    screen = QtGui.QDesktopWidget().screenGeometry()
	    size =  self.geometry()
	    self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

app = QtGui.QApplication(sys.argv)
main = MainWindow();
reply = QtGui.QMessageBox.question(main, 'message', u'问题？', QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

if reply == QtGui.QMessageBox.Yes:
	main.show()
else:
	sys.exit()

sys.exit(app.exec_())