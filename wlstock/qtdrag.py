# -*- coding: utf-8 -*-
# Created: Mon Oct 22 16:57:35 2012
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!
import sys
from PyQt4 import QtCore, QtGui ,Qt
reload(sys)
sys.setdefaultencoding("utf-8")

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_myPopForm(object):
    def setupUi(self, myPopForm):
        myPopForm.setObjectName(_fromUtf8("myPopForm"))
        myPopForm.setWindowModality(QtCore.Qt.NonModal)
        myPopForm.resize(680, 600)
        myPopForm.setStyleSheet(_fromUtf8("border:0px solid rgb(0, 0, 0);background-color: rgb(255, 255, 255);"))
        self.centralWidget = QtGui.QWidget(myPopForm)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.modelTopbar = QtGui.QLabel(self.centralWidget)
        self.modelTopbar.setGeometry(QtCore.QRect(3, 3, 774, 40))
        self.modelTopbar.setStyleSheet(_fromUtf8("background-color:#dddddd;border:0;border-bottom:0px solid #cccccc"))
        self.modelTopbar.setText(_fromUtf8(""))
        self.modelTopbar.setObjectName(_fromUtf8("modelTopbar"))
        self.closeBtn = QtGui.QPushButton(self.centralWidget)
        self.closeBtn.setGeometry(QtCore.QRect(753, 15, 15, 15))
        self.closeBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.closeBtn.setStyleSheet(_fromUtf8("border:0;background-image:url(images/top_close.png);"))
        self.closeBtn.setText(_fromUtf8(""))
        self.closeBtn.setObjectName(_fromUtf8("closeBtn"))
        self.topTitle = QtGui.QLabel(self.centralWidget)
        self.topTitle.setGeometry(QtCore.QRect(15, 15, 661, 16))
        self.topTitle.setStyleSheet(_fromUtf8("border:none;background-color:none;font: 12pt u\"微软雅黑\";"))
        self.topTitle.setObjectName(_fromUtf8("topTitle"))
        myPopForm.setCentralWidget(self.centralWidget)

        self.retranslateUi(myPopForm)
        QtCore.QObject.connect(self.closeBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), myPopForm.close)
        QtCore.QMetaObject.connectSlotsByName(myPopForm)
        #无边框
        myPopForm.setWindowFlags(Qt.Qt.FramelessWindowHint)

    def retranslateUi(self, myPopForm):
        myPopForm.setWindowTitle(u'小米粥')
        self.topTitle.setText(u'小米粥')

class renderApp(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(renderApp, self).__init__(parent)
        self.ui = Ui_myPopForm()
        self.ui.setupUi(self)
        
    def mousePressEvent(self,event):
       #鼠标点击事件
       if event.button() == QtCore.Qt.LeftButton:
           self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
           event.accept()
    def mouseMoveEvent(self,event):
       #鼠标移动事件
        if event.buttons() ==QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()   

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    render = renderApp()
    render.show()
    sys.exit(app.exec_())