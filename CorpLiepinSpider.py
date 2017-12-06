#encoding=utf-8
import os
import traceback
import urllib2
from urllib2 import Request
from bs4 import BeautifulSoup
import time
import jsonpickle


def get_industry_category_urls():

    try:


        category_urls = []

        base_url = 'https://www.liepin.com/company/converge/?categoryId={0}'

        for index in range(1, 7):
            category_urls.append(base_url.format(index) + '&curPage={0}')

	return category_urls

    except Exception, e:
	traceback.print_exc()


def get_industry_corp_list(base_url):
    try:
	page = 0
	url = base_url.format(page)
	corps = get_page_corp_list(url)
	while corps is not None and len(corps) > 0:
	    #process corps persist
	    print "collect base_url = {0}, page = {1}, corp_num = {2}".format(base_url, page, len(corps))

	    page += 1
	    url = base_url.format(page)
	    corps = get_page_corp_list(url)
	    break


    except Exception, e:
	traceback.print_exc()

def get_page_corp_list(url):
    try:
	html = urllib2.urlopen(url)
        bsObj = BeautifulSoup(html,"lxml")
        items = bsObj.findAll("a",{"class":"logo-box"})
	corps = []
	if items is not None and len(items) > 0:
	    for item in items:
		corp_info = get_corp_info(item["href"])
		corps.append(corp_info)
	return corps

    except Exception, e:
	traceback.print_exc()

def get_corp_info(url):
    try:
	print "corp_url:\t" + url
        html = urllib2.urlopen(url)
        bsObj = BeautifulSoup(html,"lxml")
	corp_name = bsObj.find("div",{"class":"name-and-welfare"}).find("h1").text.strip()
	corp_name = corp_name[:len(corp_name) - 5]
	corp_logo = bsObj.find("img",{"class":"bigELogo"})["src"]
	corp_summary = bsObj.find("p",{"class":"profile"}).text.strip()

	print "corp_name:\t"  + corp_name
	print "corp_logo:\t"  + corp_logo
#	print "corp_summary:\t"  + corp_summary
	print "*" * 120

	return {"corp_name":corp_name, "corp_logo":corp_logo, "corp_summary":corp_summary}

    except Exception, e:
	traceback.print_exc()


def download_logo(local_filename, img_url):

    try:

	res = urllib2.urlopen(Request(img_url))

	with open(local_filename,'wb') as f:
	    f.write(res.read())

    except Exception, e:
	traceback.print_exc()



category_urls = get_industry_category_urls()
for category_url in category_urls:
    print category_url
    get_industry_corp_list(category_url)
    break

#get_corp_info('https://www.liepin.com/company/1145474/')
