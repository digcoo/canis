#encoding=utf-8

#from urllib.request import urlopen
from urllib2 import urlopen
from urllib2 import Request
from bs4 import BeautifulSoup
import time


PositionDict = dict()

#PositionSet=set()


def getLinksOfPosition(BaseUrl):
	html = urlopen(BaseUrl)
	bsObj = BeautifulSoup(html,"lxml")

	PositionList = bsObj.findAll("div",{"class":"menu_sub dn"})

	for positions in PositionList:

		print ("------get all job!------")

		PositionLinkList = []
		for ddTag in positions.findAll("dd"):
		    PositionLinkList.extend(ddTag.findAll("a"))

		for PositionLink in PositionLinkList:
			#print("-"*30)
			link = PositionLink.attrs['href']
			name = PositionLink.string
			#print (link)
			#print (name)
			PositionDict[name] = link
			print (PositionDict[name])
			print (name)

def getPositionInfo(InfoUrl):

	send_headers = {
 		'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0'
	}

	req = Request(InfoUrl, headers=send_headers)

	html = urlopen(req).read()

	bsObj = BeautifulSoup(html, 'lxml')

#	print bsObj

	print ("-"*30)
	#print (bsObj.prettify())

	JobsList = bsObj.findAll("li",{"class":"con_list_item default_list"})

	for job in JobsList:

		jobName = job.h3
		jobSite = job.em
		jobTime = job.find("span",{"class":"format-time"})
		jobCompany = job.find("div",{"class":"company"}).div.a.string
		jobMoney = job.find("span",{"class":{"money"}})
		jobDemand = job.find("div",{"class":"li_b_l"})
		jobDescibe = job.find("div",{"class":"industry"})
		jobSpecial = job.find("div",{"class":"li_b_r"})

		print ("jobName:",jobName.get_text("|", strip=True))
		print ("jobSite:",jobSite.get_text("|", strip=True))
		print ("jobTime:",jobTime.get_text("|", strip=True))
		print ("jobCompany:",jobCompany)
	#	print ("jobMoney:",jobMoney.get_text("|", strip=True))
		#print ("jobDemand:",jobDemand.stripped_strings)
		i = 1
		for x in jobDemand.stripped_strings:
			if i == 1:
				print ("jobMoney:",repr(x))
			else:
				print ("jobDemand:",repr(x))
			i+=1
		print ("jobDescibe:",jobDescibe.get_text("|", strip=True))
		print ("jobSpecial:",jobSpecial.get_text("|", strip=True))
		print ("-"*30)
		time.sleep(1)

	print("-----next page!-----")
	nextLinkList = bsObj.findAll("div",{"class":"pager_container"})

	for Links in nextLinkList:
		Link = Links.findAll("a")[-1:][0]["href"]
		#print (Link)
		if Link == "javascript:;":
			print("end of job info")
			pass
		else:
			print (Link)
			getPositionInfo(Link)

		time.sleep(1)


if __name__ == '__main__':
	
	getLinksOfPosition("https://www.lagou.com/")

	count = 0
	
	for (k,v) in PositionDict.items():
		print (k)
		print (v)
		getPositionInfo(v)
		print("-"*30)
		count += 1
		time.sleep(1)
	print("-"*30)
	print(count)
	
	
	#getPositionInfo("https://www.lagou.com/zhaopin/Python/")
