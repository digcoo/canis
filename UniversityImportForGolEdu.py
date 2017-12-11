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

	base_url = 'http://ku.gol.edu.cn/index/listorder/{0}?cateid=1&typeid=1&year=2016'


	urls = []
	
	for i in range(1, 180):
	    urls.append(base_url.format(str(i)))

	return urls

    except Exception, e:
	traceback.print_exc()

def get_universities(url):

    try:


	print url

	universities = []

	html = urllib2.urlopen(url)
        bsObj = BeautifulSoup(html,"lxml")
	items = bsObj.findAll("div",{"class":"w-475"})
	for item in items:
	    univ_cn_name = item.find("a").text.strip()
	    univ_local_name = item.find("h3").text.strip()
	    univ_nation = '未知'
	    print 'univ_cn_name:\t' + univ_cn_name
	    print 'univ_local_name:\t' + univ_local_name
	    university = {"local_name":univ_local_name, "cn_name":univ_cn_name, "nation":univ_nation}
	    universities.append(university)
	    print '*' * 120
	return universities

    except Exception, e:
        traceback.print_exc()


urls = get_university_urls()

for url in urls:
    universities = get_universities(url)
#    time.sleep(2)
    MysqlClient.get_instance().add_batch_universities(universities)


#get_universities('http://ku.gol.edu.cn/index/listorder/178?cateid=1&typeid=1&year=2016')
