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

def get_universities(nation, url):

    try:

	print "base_url:\t" + url

        html = urllib2.urlopen(url)
        bsObj = BeautifulSoup(html,"lxml")
        items = bsObj.findAll("div",{"class":"gwList"})

	universities = []

	for item in items:
	    titles = item.findAll("p")
	    univ_local_name = titles[0].text[titles[0].text.find(u"：")+1:]
	    univ_cn_name = titles[2].text[titles[2].text.find(u"：")+1:]
	    universities.append({"local_name":univ_local_name, "cn_name":univ_cn_name, "nation":nation})
	    print "国外大学名称:\t" + univ_local_name
	    print "中文名称:\t" + univ_cn_name
	    print "国家:\t" + nation
	    print "*" * 100

	return universities

    except Exception, e:
	traceback.print_exc()

def compose_university_info(name):
    try:

	university_info = {}
	university_info['local_name'] = name
	university_info['cn_name'] = name

	return university_info

    except Exception, e:
        traceback.print_exc()

base_urls = {
#	"塞浦路斯":"http://www.jsj.edu.cn/n1/12021.shtml",
#	"丹麦":"http://www.jsj.edu.cn/n1/12131.shtml",
#	"英国":"http://www.jsj.edu.cn/n1/12023.shtml",
#	"马来西亚":"http://www.jsj.edu.cn/n1/12027.shtml",
#	"法国":"http://www.jsj.edu.cn/n1/12033.shtml",
#	"新西兰":"http://www.jsj.edu.cn/n1/12040.shtml",
	"波兰":"http://www.jsj.edu.cn/n1/12042.shtml"
#	"埃及":"http://www.jsj.edu.cn/n1/12045.shtml"
#	"以色列":"http://www.jsj.edu.cn/n1/12073.shtml"
#	"卢森堡":"http://www.jsj.edu.cn/n1/12095.shtml"
#	"马耳他":"http://www.jsj.edu.cn/n1/12115.shtml"
#	"捷克":"http://www.jsj.edu.cn/n1/12126.shtml"
#	"牙买加":"http://www.jsj.edu.cn/n1/12129.shtml",
#	"克罗地亚":"http://www.jsj.edu.cn/n1/12130.shtml",
#	"哥斯达黎加":"http://www.jsj.edu.cn/n1/12132.shtml",
#	"摩纳哥":"http://www.jsj.edu.cn/n1/12133.shtml",
#	"斯洛文尼亚":"http://www.jsj.edu.cn/n1/12134.shtml",
#	"格林纳达":"http://www.jsj.edu.cn/n1/12135.shtml"
	}

for nation in base_urls.keys():
    universities = get_universities(nation, base_urls[nation])
#    time.sleep(2)
    MysqlClient.get_instance().add_batch_universities(universities)
