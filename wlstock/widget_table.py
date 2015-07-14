#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore

class widget_table(QtGui.QTableWidget):
	"""docstring for widget_table"""
	def __init__(self, parent = None):
		QtGui.QTableWidget.__init__(self, parent)
		self.catch = False 
		self.parent = parent
	
	#支持窗口拖动,重写两个方法
	def mousePressEvent(self, event):
		#鼠标点击事件
		
		if event.button() == QtCore.Qt.LeftButton:
			self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
			event.accept()
		if event.button() == QtCore.Qt.RightButton:
			print 'rightbutton'

	def contextMenuEvent(self, event):
		if not self.catch:
			return QtGui.QTableWidget.keyPressEvent(self, event)

		self._moveCursor(event.key())

	def _moveCursor(self, key):
		row = self.currentRow()
		col = self.currentColumn()

		if key == Qt.Key_Left and col > 0:
			col -= 1

		elif key == Qt.Key_Right and col < self.columnCount():
			col += 1

		elif key == Qt.Key_Up and row > 0:
			row -= 1

		elif key == Qt.Key_Down and row < self.rowCount():
			row += 1

		else:
			return

		self.setCurrentCell(row, col)
		self.edit(self.currentIndex())

	#支持窗口拖动,重写两个方法
	def mousePressEvent(self, event):
		#鼠标点击事件
		if event.button() == QtCore.Qt.LeftButton:
			self.parent.mousePressEvent(event)
			# self.parent.dragPosition = event.globalPos() - self.parent.frameGeometry().topLeft()
			# event.accept()
 
	def mouseMoveEvent(self, event):
		if event.buttons() ==QtCore.Qt.LeftButton:
			self.parent.mouseMoveEvent(event)
			# self.parent.move(event.globalPos() - self.parent.dragPosition)
			# event.accept()