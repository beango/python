#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, re, threading, os
import urllib2, sqlite3
from PyQt4 import QtGui, QtCore
from dbutil import DbUtil
from TimerClass import TimerClass
from PyQt4.Qt import *
import getk
from StockUtil import StockUtil
from LRUCache import LRUCache
from widget_table import widget_table

reload(sys)
sys.setdefaultencoding("utf-8")
cache = LRUCache(100)
dbutil = DbUtil()
cachekey = 'mystock_cuall'
from qtdrag import Ui_myPopForm

class MainWindow(QtGui.QMainWindow):
	def __init__(self, parent=None):
		# QtGui.QMainWindow.__init__(self, None
  		#  		       ,QtCore.Qt.WindowStaysOnTopHint |
  		#  		       QtCore.Qt.FramelessWindowHint)
		super(MainWindow, self).__init__(parent)
		self.titleHeight = 0
		self.headHeight = 22
		self.rowHeight = 33
		self.width = 450
		self.ui = Ui_myPopForm()
		self.ui.setupUi(self)
		self.resize(self.width, 300)
		self.sortcol = 0

		'''
		self.setMouseTracking(True)
		self.setWindowTitle(u'窗口标题')
		#self.center();
		'''
		tbcols = [u'股票代码',u'股票名称',u'最新价',u'涨跌额',u'涨跌幅',u'最高价',u'最低价']
		self.tbl = self.crttable(self.ui.centralWidget, tbcols)
		self.tbl.setGeometry(QtCore.QRect(0, self.titleHeight, self.width, 300))
		self.delayrun()
		self.timer=QtCore.QTimer()
		QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.delayrun)
		self.timer.start(3000)
		
	#支持窗口拖动,重写两个方法
	def mousePressEvent(self, event):
		#鼠标点击事件
		if event.button() == QtCore.Qt.LeftButton:
			self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
			event.accept()
 
	def mouseMoveEvent(self, event):
		if event.buttons() ==QtCore.Qt.LeftButton:
			self.move(event.globalPos() - self.dragPosition)
			event.accept()
	
	def slot_sortByColumn(self, idx):
		print 'slot_sortByColumn()', idx

	def VerSectionClicked(self,index):
		self.sortcol = index

	def HorSectionClicked(self,index):
		self.sortcol = index
		self.delayrun()

	def crttable(self, target, tbcols):
		tb = widget_table(target)
		tb.setColumnCount(len(tbcols))
		tb.setHorizontalHeaderLabels(tbcols)  
		
		QtCore.QObject.connect(tb,QtCore.SIGNAL("itemSelectionChanged()"), self.itemSelectionChanged)
		tb.setSortingEnabled(True)
		# tb.verticalHeader().sectionClicked.connect(self.VerSectionClicked)#表头单击信号
		tb.horizontalHeader().sectionClicked.connect(self.HorSectionClicked)#表头单击信号

		tb.installEventFilter(self)
		
		for x in range(tb.columnCount()):  
			headItem = tb.horizontalHeaderItem(x)   		#获得水平方向表头的Item对象  
			headItem.setBackgroundColor(QColor(0,60,10))    #设置单元格背景颜色  
			headItem.setTextColor(QColor(200,111,30))       #设置文字颜色 
		
		tb.horizontalHeader().resizeSection(0,60)
		tb.horizontalHeader().resizeSection(1,90)
		tb.horizontalHeader().resizeSection(2,60)
		tb.horizontalHeader().resizeSection(3,60)
		tb.horizontalHeader().resizeSection(4,60)
		tb.horizontalHeader().resizeSection(5,60)
		tb.horizontalHeader().resizeSection(6,60)

		#设置表头字体加粗
		font = tb.horizontalHeader().font()
		font.setBold(True)
		tb.horizontalHeader().setFont(font)
		tb.horizontalHeader().setStretchLastSection(True) #设置充满表宽度

		tb.verticalHeader().setDefaultSectionSize(0) #设置行距
		tb.setFrameShape(False) #设置无边框
		tb.setShowGrid(False) #设置不显示格子线
		tb.verticalHeader().setVisible(False) #设置垂直头不可见
		tb.horizontalHeader().setVisible(True) #隐藏行表头
		# table_widget->setSelectionMode(QAbstractItemView::ExtendedSelection); //可多选（Ctrl、Shift、 Ctrl+A都可以）
		tb.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)  #禁止编辑
		tb.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)  #整行选中的方式
		# table_widget->horizontalHeader()->resizeSection(0,150); //设置表头第一列的宽度为150
		tb.horizontalHeader().setFixedHeight(self.headHeight) #设置表头的高度
		# table_widget->setStyleSheet("selection-background-color:lightblue;"); //设置选中背景色
		tb.horizontalHeader().setStyleSheet("QHeaderView::section{background:black;}"); #设置表头背景色

		# 设置水平、垂直滚动条样式
		# table_widget->horizontalScrollBar()->setStyleSheet("QScrollBar{background:transparent; height:10px;}"
		# "QScrollBar::handle{background:lightgray; border:2px solid transparent; border-radius:5px;}"
		# "QScrollBar::handle:hover{background:gray;}"
		# "QScrollBar::sub-line{background:transparent;}"
		# "QScrollBar::add-line{background:transparent;}");
		# table_widget->verticalScrollBar()->setStyleSheet("QScrollBar{background:transparent; width: 10px;}"
		# "QScrollBar::handle{background:lightgray; border:2px solid transparent; border-radius:5px;}"
		# "QScrollBar::handle:hover{background:gray;}"
		# "QScrollBar::sub-line{background:transparent;}"
		# "QScrollBar::add-line{background:transparent;}");

		#点击表时不对表头行光亮（获取焦点） 
		tb.horizontalHeader().setHighlightSections(False);


		return tb

	
	def itemSelectionChanged(self):
		pass

	def eventFilter(self, source, event):
		if (event.type() == QtCore.QEvent.KeyPress):
			key = event.key()
			if key == QtCore.Qt.Key_A:
				stock,ok=QInputDialog.getText(self,u"添加",  u"股票代码:",  QLineEdit.Normal,'')  
				if ok and (not stock.isEmpty()):  
					self.addstock(str(stock))  
			if key == QtCore.Qt.Key_D:
				selectedItems = self.tbl.selectedItems()
				if len(selectedItems)!=0:
					msgbox=QMessageBox.question(self, u'提示', u'确认要删除吗？', QMessageBox.Ok|QMessageBox.Cancel, 
						QMessageBox.Ok)
					if msgbox==QMessageBox.Ok:
						stock = str(selectedItems[0].text())
						dbutil.delstock(stock)
						cache.remove(cachekey)
			if key == QtCore.Qt.Key_I:
				selectedItems = self.tbl.selectedItems()
				if len(selectedItems)!=0:
					stock = (str(selectedItems[0].text()))[0:6]
					stocktype = stockutil.getstocktyp(stock)
					dlg = Stock2(self,stocktype,stock)
					dlg.exec_()
			if key == QtCore.Qt.Key_Q:
				sys.exit()
			
		return QtGui.QMainWindow.eventFilter(self, source, event)

	def addstock(self, stock):
		res = stockutil.chkstock(stock)
		if res[0] == True:
			if dbutil.insertone(res[1], res[2]) == False:
				print u'已经存在'
			else:
				cache.remove(cachekey)
		else:
			print u'添加失败'

	def center(self):
	    screen = QtGui.QDesktopWidget().screenGeometry()
	    size =  self.geometry()
	    self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

	def getstock(self, stockno, stocktype):
		pattern = re.compile(r'"(.*)"')
		sinfo = urllib2.urlopen('http://hq.sinajs.cn/list='+stocktype+stockno).read()
		#sinfo="var hq_str_sh000001=\"上证指数,4604.579,4576.492,4690.150,4691.768,4552.129,0,0,543003709, 
		#815062691654,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2015-06-24,15:04:04,00\""
		match = pattern.split(sinfo)
		sinfo = match[1]
		ssplit = sinfo.split(',')
		return (ssplit[0].decode("gbk"), ssplit[3], ssplit[2])

	def delayrun(self): 
		stocklist = cache.get(cachekey);
		if stocklist==None:
			stocklist = dbutil.getall()
			cache.set(cachekey,stocklist)

		self.tbl.setRowCount(len(stocklist)) 
		for x in xrange(1,self.tbl.rowCount()+1):
			self.tbl.setRowHeight(x,self.rowHeight)
		idx = 0
		stockliststr = ""
		for stockitem in stocklist:
			stock = stockitem[1]
			stocktype = stockitem[2]
			stockliststr += ","+stocktype+stock+""
		if(stockliststr!=""):
			stocklistinfo = stockutil.getstockbatch(stockliststr[1:]) #获取stock
			sortcolnam = ''
			if self.sortcol == 0:
				sortcolnam = 'stockno'
			if self.sortcol == 1:
				sortcolnam = 'stockname'
			if self.sortcol == 2:
				sortcolnam = 'nowprice'
			if self.sortcol == 3:
				sortcolnam = 'zde'
			if self.sortcol == 4:
				sortcolnam = 'zdf'
			if self.sortcol == 5:
				sortcolnam = 'todaymaxprice'
			if self.sortcol == 6:
				sortcolnam = 'todayminprice'
			stocklistinfo.sort(lambda x,y : cmp(x[sortcolnam], y[sortcolnam]))
			for stockitem in stocklistinfo:
				stockno = stockitem["stockno"]
				stocktype = stockitem["stocktype"]
				stockname = stockitem['stockname'] # 		
				stockname = stockname+'.'+stocktype #股票名称  
				nowprice = stockitem["nowprice"] # 最新价
				yesendprice = stockitem["yesendprice"] # 前收盘价
				todaymaxprice = stockitem["todaymaxprice"] # 前收盘价
				todayminprice = stockitem["todayminprice"] # 前收盘价
				c1 = QtGui.QColor(0,238,0)# 绿
				c2 = QtGui.QColor(255,0,0)#红
				c3 = QtGui.QColor(255,255,255)#白
				c4 = QtGui.QColor(0,0,0)#黑
				
				#股票代码
				stockItem = QtGui.QTableWidgetItem(stockitem["stockno"]) 
				stockItem.setBackgroundColor(c4) 
				stockItem.setTextColor(c3) 
				stockItem.setTextAlignment(QtCore.Qt.AlignHCenter |  QtCore.Qt.AlignVCenter) #水平对齐
				self.tbl.setItem(idx, 0, stockItem) 

				#股票名称  
				stocknoItem = QtGui.QTableWidgetItem(stockname) # 股票名称
				stocknoItem.setBackgroundColor(c4)
				stocknoItem.setTextColor(c3) 
				stocknoItem.setTextAlignment(QtCore.Qt.AlignHCenter |  QtCore.Qt.AlignVCenter) #水平对齐
				self.tbl.setItem(idx, 1, stocknoItem)  

				# 最新价
				nowpriceItem = QtGui.QTableWidgetItem(str(nowprice))  
				nowpriceItem.setBackgroundColor(c4)
				nowpriceItem.setTextColor(c3) 
				nowpriceItem.setTextAlignment(QtCore.Qt.AlignHCenter |  QtCore.Qt.AlignVCenter) #水平对齐
				self.tbl.setItem(idx, 2, nowpriceItem) 

				# 涨跌额
				zdf = nowprice-yesendprice
				if nowprice==0:
					zdf = ""
				zdItem = QtGui.QTableWidgetItem(str(stockitem["zde"]))  
				zdItem.setBackgroundColor(c4)
				zdItem.setTextColor(c1) 
				zdItem.setTextAlignment(QtCore.Qt.AlignHCenter |  QtCore.Qt.AlignVCenter)
				self.tbl.setItem(idx, 3, zdItem) 
				
				# 涨跌幅
				zdfItem = QtGui.QTableWidgetItem(str(stockitem["zdf"])+'%')  
				zdfItem.setBackgroundColor(QtGui.QColor(0,0,0))
				zdfItem.setTextColor(c1) 			
				if nowprice>0 and zdf>0:
					zdItem.setTextColor(c2) 
					zdfItem.setTextColor(c2) 
				elif nowprice>0 and zdf<0:
					zdItem.setTextColor(c1) 
					zdfItem.setTextColor(c1) 
				else:
					zdItem.setTextColor(c3) 
					zdfItem.setTextColor(c3) 
				zdfItem.setTextAlignment(QtCore.Qt.AlignHCenter |  QtCore.Qt.AlignVCenter)
				self.tbl.setItem(idx, 4, zdfItem) 

				# 最高价
				todaymaxpriceItem = QtGui.QTableWidgetItem(str(todaymaxprice))  
				todaymaxpriceItem.setBackgroundColor(c4)
				todaymaxpriceItem.setTextColor(c3) 
				todaymaxpriceItem.setTextAlignment(QtCore.Qt.AlignHCenter |  QtCore.Qt.AlignVCenter)
				self.tbl.setItem(idx, 5, todaymaxpriceItem) 

				# 最新价
				todayminpriceItem = QtGui.QTableWidgetItem(str(todayminprice))  
				todayminpriceItem.setBackgroundColor(c4)
				todayminpriceItem.setTextColor(c3) 
				todayminpriceItem.setTextAlignment(QtCore.Qt.AlignHCenter |  QtCore.Qt.AlignVCenter)
				self.tbl.setItem(idx, 6, todayminpriceItem) 
				idx+=1
		#def end
		self.tbl.verticalHeader().setResizeMode(QHeaderView.ResizeToContents)
		self.tbl.setContextMenuPolicy(Qt.CustomContextMenu);  
		self.tbl.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff);  
		# for x in xrange(1,self.tbl.rowCount()):
		height = self.tbl.rowCount() * self.tbl.rowHeight(1) + self.headHeight;
		self.resize(self.width, height);
		# self.tbl.sortByColumn(4)

class Stock2(QtGui.QDialog):
	def __init__(self, parent, stocktype, stockno):
		super(Stock2, self).__init__(parent)
		self.resize(200, 200)
		settings = QSettings()
		self.image=QImage()  
		imgpath = 'newchart/daily/n/'+stocktype+stockno+'.gif'
		if not os.path.isfile(imgpath):
			url = "http://image.sinajs.cn/newchart/daily/n/"+stocktype+stockno+".gif";
			res = urllib2.urlopen(url).read()
			if not os.path.exists("newchart/daily/n/"):
				os.makedirs("newchart/daily/n/")
			open('newchart/daily/n/'+stocktype+stockno+'.gif', 'wb').write(res)
		if self.image.load('newchart/daily/n/'+stocktype+stockno+'.gif'):  
			self.imageLabel=QLabel()  
			self.imageLabel.setPixmap(QPixmap.fromImage(self.image))  
			self.resize(self.image.width(),self.image.height())  
			
			toolPathGroupBox = QGroupBox(u"")
			pathsLayout = QGridLayout()
			pathsLayout.addWidget(self.imageLabel, 0, 0)
			toolPathGroupBox.setLayout(pathsLayout)

			layout = QVBoxLayout()
			layout.addWidget(toolPathGroupBox)
			self.setLayout(layout)

class MyPopup(QtGui.QDialog):
	def __init__(self, parent=None):
		super(MyPopup, self).__init__()
		self.resize(100, 100)
		settings = QSettings()
		self.snotxt = QtGui.QTextEdit()
		self.snotxt.setLineWrapMode(QTextEdit.WidgetWidth)
		addButton = QPushButton(u"&添加")
		toolPathGroupBox = QGroupBox(u"")
		pathsLayout = QGridLayout()
		pathsLayout.addWidget(self.snotxt, 0, 0)
		pathsLayout.addWidget(addButton, 0, 1)
		toolPathGroupBox.setLayout(pathsLayout)

		layout = QVBoxLayout()
		layout.addWidget(toolPathGroupBox)
		self.setLayout(layout)
		self.connect(addButton, SIGNAL("clicked()"), self.click)
    
	def click(self):
		res = stockutil.chkstock(str(self.snotxt.toPlainText()))
		if res[0] == True:
			if dbutil.insertone(res[1], res[2]) == False:
				print u'已经存在'
			else:
				cache.remove(cachekey)
				QDialog.accept(self)
		else:
			print u'添加失败'

def listenKey():
    while True:
    	print 'Press a key'
    	inkey = getk._Getch()
    	for i in xrange(sys.maxint):
	 	k=inkey()
	 	if k <> '': break
    	print 'you pressed ',k
    	if k == 'i':
			tmr.stop()
			os.system("cls")
			stockno = raw_input(u"input stock no: ")
			while True:
				sno = stockno
				res = stockutil.chkstock(sno)
				if res[0] == True :
					if dbutil.insertone(res[1], res[2]) == False:
						print u'已经存在'
						stockno = raw_input(u"input stock no: ")
					tmr.resume()
					return
				stockno = raw_input(u"input stock no: ")
    	elif k == 'q':
			print 'q'
			os.system("exit")
		 	return

if __name__=="__main__":
	stockutil = StockUtil()
	app = QtGui.QApplication(sys.argv)
	main = MainWindow();
	main.show()
	sys.exit(app.exec_())


