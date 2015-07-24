#-*- coding: utf-8 -*-

import single_ui,singleTime
from PyQt4 import QtCore, QtGui
import time

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtGui.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig)

class thread_Check(QtCore.QThread):
	def __init__(self,number):
		super(thread_Check, self).__init__()
		self.chk = singleTime.GetData(number)
	def run(self):
		self.chk.randomCookie()
		self.chk.getCHA()
		self.chk.getData()

class Checker(single_ui.Ui_MainWindow):
	def __init__(self):
		super(Checker, self).__init__()
		self.setupUi(self)
		self.pushButton.clicked.connect(self.Run)

	def Run(self):
		self.pushButton.setDisabled(True)
		self.textEdit.clear()
		self.textEdit.setAlignment(QtCore.Qt.AlignCenter)
		number = self.lineEdit.text()
		if len(number) != 10 :
			QtGui.QMessageBox.critical(self, ' ', _translate("MainWindow", "考号错误！", None))
			self.pushButton.setDisabled(False)
			return False
		else:
			number = number.toInt()[0]
			self.progressBar.setVisible(True)
			self.progressBar.setValue(0)
			self.tem = thread_Check(number)
			self.tem.chk.addprocess.connect(self.setValue)
			self.tem.chk.finished.connect(self.done)
			self.tem.start()

	def setValue(self,v):
		self.progressBar.setValue(v)

	def done(self, data):
		self.progressBar.setValue(100)
		time.sleep(1)
		self.progressBar.setVisible(False)

		sentence = QtCore.QString()
		for item in data:
			sentence = sentence + _translate("MainWindow", item+'\n', None)

		self.textEdit.setText(sentence)
		self.pushButton.setDisabled(False)

if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	MainWindow = Checker()
	MainWindow.show()
	sys.exit(app.exec_())
