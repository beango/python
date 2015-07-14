#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import *
 
def sinTest():
    btn.setText(u"按钮文本改变")
 
app = QApplication([])
 
main = QWidget()
main.resize(200,100)
btn = QPushButton(u"按钮文本",main)
##按钮btn的内置信号连接名为sinTest的槽
btn.clicked.connect(sinTest)
main.show()
 
app.exec_()