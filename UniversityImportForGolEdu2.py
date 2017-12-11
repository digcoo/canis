#encoding=utf-8
import os
import traceback
import urllib2
from urllib2 import Request
from bs4 import BeautifulSoup
import time
from MysqlClient import *

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def get_university_urls():

    try:

	urls = {}
#	urls["澳大利亚"] = "http://fair.shie.edu.cn/slists/slists/index/?country=AU"
#	urls["美国"] = "http://fair.shie.edu.cn/slists/slists/index/?country=US"
#	urls["英国"] = "http://fair.shie.edu.cn/slists/slists/index/?country=GB"
#	urls["加拿大"] = "http://fair.shie.edu.cn/slists/slists/index/?country=CA"
	urls["未知"] = "http://fair.shie.edu.cn/slists/slists/index/?country=NLMT"
	return urls

    except Exception, e:
	traceback.print_exc()

def get_universities_for_page(url, nation):

    try:


	print url

	universities = []

	html = urllib2.urlopen(url)
        bsObj = BeautifulSoup(html,"lxml")
	items = bsObj.find("div",{"class":"list-main mg"}).findAll("dl")
	for item in items:
	    univ_cn_name = item.find("dd").find("a").text.strip()
	    univ_local_name = item.find("p").text.strip()
	    univ_logo = "http://fair.shie.edu.cn" + item.find("img")["src"]
	    univ_nation = nation
	    print 'univ_cn_name:\t' + univ_cn_name
	    print 'univ_local_name:\t' + univ_local_name
	    print 'univ_logo:\t' + univ_logo
	    university = {"local_name":univ_local_name, "cn_name":univ_cn_name, "nation":univ_nation, "logo":univ_logo}
	    universities.append(university)
	    print '*' * 120
	return universities

    except Exception, e:
        traceback.print_exc()


def get_universities(url, nation):

    try:

	universities = []

	page = 1
	req_url = (url + "&per_page={0}").format(page)
	page_universities = get_universities_for_page(req_url, nation)
	while page_universities is not None and len(page_universities) > 0 and page < 10:
	    universities.extend(page_universities)
	    time.sleep(3)

	    page = page + 1
	    req_url = (url + "&per_page={0}").format(page)
	    page_universities = get_universities_for_page(req_url, nation)
	    
	return universities


    except Exception, e:
        traceback.print_exc()


urls = get_university_urls()

for nation in urls.keys():
    universities = get_universities(urls[nation], nation)
    print len(universities)
    MysqlClient.get_instance().add_batch_universities(universities)


#get_universities('http://ku.gol.edu.cn/index/listorder/178?cateid=1&typeid=1&year=2016')
