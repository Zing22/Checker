#-*- coding: utf-8 -*-

import requests,time,random
from PyQt4 import QtCore,QtGui

class GetData(QtGui.QWidget):
	addprocess = QtCore.pyqtSignal(float)
	finished = QtCore.pyqtSignal(list)

	def __init__(self, number):
		super(GetData, self).__init__()
		self.number = number
		self.flag = False
		self.code = None

	def randomCookie(self):
		l = [chr(x) for x in xrange(97,123)] + [chr(x) for x in xrange(48,58)]
		cookie = ''.join(random.sample(l,26)).replace(' ','')
		print 'Random cookie:',cookie
		self.addprocess.emit(2)
		self.psid = cookie
		self.cookies = {
			'PHPSESSID': self.psid,\
			'Hm_lvt_2be31ff7176cef646e9351788dc99055':'1437108237,1437197089,1437199631,1437541063',\
			'Hm_lpvt_2be31ff7176cef646e9351788dc99055':'1437542800',\
		}
		self.header = {
			'Accept':'application/json, text/javascript, */*; q=0.01',\
			'Accept-Encoding':'gzip, deflate',\
			'Accept-Language':'zh-CN,zh;q=0.8',\
			'Connection':'keep-alive',\
			'Content-Length':'31',\
			'Content-Type':'application/x-www-form-urlencoded',\
			'Host':'www.5184.com',\
			'Origin':'http://www.5184.com',\
			'Referer':'http://www.5184.com/gk/check_lq.html',\
			'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',\
			'X-Requested-With':'XMLHttpRequest',\
			'Cookie':'PHPSESSID=%s; Hm_lvt_2be31ff7176cef646e9351788dc99055=1437108237,1437197089,1437199631,1437541063; Hm_lpvt_2be31ff7176cef646e9351788dc99055=1437542800'% self.psid,\
		}
		return

	def getCHA(self):
		print 'Getting code pic...'
		url = 'http://www.5184.com/gk/common/checkcode.php'
		res = requests.get(url,params={'r':'0.6292654476128519'},cookies=self.cookies)
		print 'Got code!'
		self.addprocess.emit(5)
		return self.guessCHA()

	def guessCHA(self):
		print "Begin to guess!"
		geussUrl = 'http://www.5184.com/gk/common/get_lq_edg.php'
		for c in xrange(0,19):
			guessData = {
				'csny':'9711',\
				'zkzh':'1402106034',\
				'yzm':str(c),\
			}
			guessDic = dict()
			try:
				guessDic = requests.post(geussUrl,data=guessData,headers=self.header,cookies=self.cookies).json()
			except Exception,e:
				print e
				print guessDic
			if 'result' in guessDic:
				self.code = str(c)
				print "Got CODE: %s! Ready to RUN!!!" % self.code
				self.addprocess.emit(20)
				return True
			else:
				self.addprocess.emit(5 + 15.0 * (c+1)/18.0)
		print "Guess Fail..."
		return False

	def getData(self):
		posturl = 'http://www.5184.com/gk/common/get_lq_edg.php'
		birthdayYears = ('97', '96', '98', '95', '94', '98')
		birthdayMonth = ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12')
		self.flag = False
		self.times = 0
		for year in birthdayYears:
			for month in birthdayMonth:
				self.times += 1
				if self.flag:
					continue
				postData = {
					'csny':year+month,\
					'zkzh':self.number,\
					'yzm':self.code,\
				}
				print 'tyring: (%s, %s)' % (self.number,year+month)
				dic = requests.post(posturl,data=postData,headers=self.header,cookies=self.cookies).json()
				if dic[u'flag']:
					try:
						dic = dic['result']
						print u'~~~ ** Got Data!!! ** ~~~'
						self.flag = True
						dataList = [dic['xm'],dic['zkzh'],dic['lbm'],dic['zymc'],dic['pcm'],"--- END ---"]
						self.addprocess.emit(100)
						self.finished.emit(dataList)
					except Exception,e:
						print e
				else:
					print "Wrong birthday,trying again..."
					print dic['msg']
					self.addprocess.emit(20 + 80.0 * (self.times)/72.0)
		if not self.flag:
			print "** -- No Data! -- **"
			self.finished.emit(["暂无该考生数据。", "--- END ---"])

		return False

if __name__ == '__main__':
	import sys
	app = QtGui.QApplication(sys.argv)
	l = GetData(1402206628)
	l.randomCookie()
	if l.getCHA():
		l.getData()








