#-*- coding: utf-8 -*-

import requests,time,random

class GetData(object):
	def __init__(self, NumFile, NotDoneFile, DoneFile, LastOne=None):
		self.randomCookie()
		self.numberls = list()
		f = open(NumFile)
		for item in f.readlines():
			self.numberls.append(item.strip())
		f.close
		self.NotDoneFileName = NotDoneFile
		self.DoneFileName = DoneFile
		self.flag = False
		self.lastOne = str(LastOne)
		self.code = None

	def __del__(self):
		print "DELTET this object!"
		f = open('lastOne.txt','wb')
		f.write(self.lastOne)
		f.close()

	def randomCookie(self):
		l = [chr(x) for x in xrange(97,123)] + [chr(x) for x in xrange(48,58)]
		cookie = ''.join(random.sample(l,22)).replace(' ','')
		print 'Random cookie:',cookie
		time.sleep(3)
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

	def getCHA(self,name=None):
		print 'Getting code pic...'
		url = 'http://www.5184.com/gk/common/checkcode.php'
		res = requests.get(url,params={'r':'0.3591778995934874'},cookies=self.cookies)
		#f = file("%s.jpg"%name,'wb')
		#f.write(res.content)
		#f.close()
		print 'Got code!'
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
			guessDic = requests.post(geussUrl,data=guessData,headers=self.header,cookies=self.cookies).json()
			if 'result' in guessDic:
				self.code = str(c)
				print "Got CODE: %s! Ready to RUN!!!" % self.code
				time.sleep(3)
				return True
		print "Guess Fail..."
		return False

	def getData(self):
		self.numberls = self.numberls[self.numberls.index(self.lastOne):]
		self.NotDoneFile = open(self.NotDoneFileName,'a')
		self.DoneFile = open(self.DoneFileName,'a')
		posturl = 'http://www.5184.com/gk/common/get_lq_edg.php'
		birthdayYears = ('97', '96', '98', '95')
		birthdayMonth = ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12')
		for number in self.numberls:
			self.flag = False
			self.lastOne = number
			print 'tyring: %s' % number
			for year in birthdayYears:
				for month in birthdayMonth:
					if self.flag:
						continue
					postData = {
						'csny':year+month,\
						'zkzh':number,\
						'yzm':self.code,\
					}
					try:
						dic = requests.post(posturl,data=postData,headers=self.header,cookies=self.cookies).json()
					except:
						self.NotDoneFile.close()
						self.DoneFile.close()
						return (True,self.lastOne)
					if dic[u'flag']:
						try:
							dic = dic['result']
							print u'~~~ ** Got Data!!! ** ~~~'
							self.flag = True
							str1 = '%s %s %s\n%s %s\n-------\n' % (dic['xm'],dic['zkzh'],dic['lbm'],dic['zymc'],dic['pcm'])
							self.DoneFile.write(str1.encode("utf-8"))
						except Exception,e:
							print e
			if not self.flag:
				print "** -- No Data! -- **"
				self.NotDoneFile.write(number+'\n')

		self.NotDoneFile.close()
		self.DoneFile.close()
		return (False,self.lastOne)

if __name__ == '__main__':
	isworking = True
	temLast = raw_input('LastOne is:')
	while(isworking):
		try:
			l = GetData('numbers.txt','NotDone.txt','Done.txt')
			print "Build a new object!"
			l.lastOne = temLast
			if l.getCHA():
				(isworking,temLast) = l.getData()
			else:
				print 'Got CHA Error!'
				continue
			try:
				temLast = l.lastOne
			except:
				print "Object was deleted..."
		except Exception,e:
			print "lastOne:", l.lastOne
			print e
			temLast = l.lastOne








