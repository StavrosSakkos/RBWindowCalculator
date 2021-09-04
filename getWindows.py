import time,os,datetime,sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

A = ["Valakas"]
B = ["Antaras","Baium","Queen Ant",]
C = ["Core","Orfen","Zaken"]
D = ["Blinding Fire Barakiel"]
ignoreList = ["Warden Guillotine","Heart Of Volcano","Carnage Lord Gato"\
	,"Ancient Weird Drake","Greyclaw Kutus","Carnage Lord Gato","Heart Of Warding"\
	,"Antharas Epic Controller", "Baium Epic Controller", "Core Epic Controller"\
	,"Orfen Epic Controller", "Qa Epic Controller", "Valakas Epic Controller"\
	,"Zaken Epic Controller"]
E = ["Golkonda Longhorn","Domb Death Cabrio","Hallate The Death Lord","Kernon"]
F = ["It Bloody Tree Vermilion","It Cherub Garacsia","It Ketra Chief Brakki","It Last Lesser Glaki"\
	,"It Shuriel Fire Of Wrath","It Varka Commnder Mos","It Varka Hero Shadith","Korim"]

#SITE = ""
OFFSET = 30
options = Options()
options.add_argument("--headless")

def printLists(aliveList,deadList,restList,testList):
	if not aliveList and not deadList:
		print("================EMPTY================")
		return
	print("=====================================")
	print("================START================")
	print(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
	if aliveList:
		print("=============== ALIVE ===============")
	for i in aliveList:
		print(i[0],i[1])
	print()
	if deadList:
		print("============= IN WINDOW =============")
	for i in deadList:
		print(i[0])
		print("T.o.D :",i[1]," || Passed :",i[3]," || Remaining Window : ",i[2]," || Percentage :",\
			str(round(getProbability(i[3],i[0])*100,2))+"%")
	if testList:
		print("=========== CLOSE TO WINDOW ===========")
	for i in testList:
		print(i[0])
		print("T.o.D :",i[1]," || In window in :",\
			datetime.timedelta(minutes=OFFSET) - datetime.timedelta(minutes=getRBWindow(i[0])[1]) + i[2])
	print("=================END=================")
	print("=====================================")

def getWindow(dateTimeNow,timeOfDeath):
	return dateTimeNow - datetime.timedelta(hours = 1) \
		- toDateTime(timeOfDeath)

def getProbability(countdown,nameOfRb):
	h,w = getRBWindow(nameOfRb)
	return ((countdown - datetime.timedelta(hours = h) +\
		 datetime.timedelta(minutes = w)).total_seconds()) / (2*w*60)

def toDateTime(strng):
	return datetime.datetime.strptime(strng,'%Y-%m-%d %H:%M:%S')

def getRBWindow(nameOfRb):
	if nameOfRb in A:
		return 172,30
	elif nameOfRb in B:
		return 72,30
	elif nameOfRb in C:
		return 42,30
	elif nameOfRb in D:
		return 14,0
	elif nameOfRb in E:
		return 8,120
	elif nameOfRb in F:
		return 12,120
	elif not nameOfRb in ignoreList:
		return 10,120
	return 0,0

def checkIfInWindow(dt,dm):
	if dt <= datetime.timedelta(minutes = dm) and \
		dt >= -datetime.timedelta(minutes = dm):
			return True
	return False

def getCountdown(dtTimedelta,dif,dh):
	return datetime.timedelta(hours = dh) - dif

def getRBLists(L):
	returnAliveList,returnDeadList,restOfTheList = list(),list(),list()
	returnTestList = list()
	for row in L:
		cols = row.find_all('td')
		cols = [x.text.strip() for x in cols]
		print(cols)
		dh,dm = getRBWindow(cols[0])
		if cols[1] in ["Dead","Muerto","Morto"] and not dh == 0:
			dateTimeNow = datetime.datetime.now()
			dif = getWindow(dateTimeNow,cols[2])
			if checkIfInWindow(datetime.timedelta(hours = dh) - dif,dm):
				returnDeadList.append([cols[0],cols[2],\
					datetime.timedelta(hours = dh) - dif + datetime.timedelta(minutes = dm),dif])
			elif checkIfInWindow(datetime.timedelta(hours = dh) - dif - datetime.timedelta(minutes = OFFSET),dm):
				returnTestList.append([cols[0],cols[2],\
					datetime.timedelta(hours = dh) - dif - datetime.timedelta(minutes = OFFSET)])
			else:
				restOfTheList.append([cols[0],cols[2],datetime.timedelta(hours = dh) - dif])
		else:
			if not dh == 0:
				returnAliveList.append([cols[0],cols[1]])
	return returnAliveList,returnDeadList,restOfTheList,returnTestList

def popUseless(L):
	L.pop(0)
	if L[len(L)-1] == "" or L[len(L)-1] == "-":
		L.pop(len(L)-1)

def main(usrnm,passwd,SITE):
	try:
		browser = webdriver.Chrome(options=options)
		browser.get(SITE)
		username = browser.find_element_by_name("ucp_login")
		password = browser.find_element_by_name("ucp_passw")
		username.send_keys(usrnm)
		password.send_keys(passwd)
		browser.find_element_by_class_name("accessButton").click()
		browser.get(SITE)
		html = browser.page_source
		os.system("cls" if os.name=="nt" else "clear")
		bs = BeautifulSoup(html, "lxml")
		table_body=bs.find('tbody')
		L = table_body.find_all('tr')
		popUseless(L)
		aL,dL,rL,tL = getRBLists(L)
		printLists(aL,dL,rL,tL)
		browser.close()
		time.sleep(10)
	except KeyboardInterrupt:
		print("Quitting...")
		sys.exit(0)

if __name__ == "__main__":
	usrnm = "username here!"
	passwd = "password here!"
	site = input("Link: ")
	#while(True):
	main(usrnm,passwd,site)
