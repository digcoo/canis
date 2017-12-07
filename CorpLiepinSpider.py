#encoding=utf-8
import os
import traceback
import urllib
import urllib2
from urllib2 import Request
from bs4 import BeautifulSoup
import time
import jsonpickle
from MysqlClient import *

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
	page = 22
	url = base_url.format(page)
	corps = get_page_corp_list(url)
	print "collect base_url = {0}, page = {1}, corp_num = {2}".format(base_url, page, len(corps))
	while corps is not None and len(corps) > 0:
	    #process corps persist
	    MysqlClient.get_instance().add_batch_corps(corps)
	    print "collect base_url = {0}, page = {1}, corp_num = {2}".format(base_url, page, len(corps))

	    page += 1
	    url = base_url.format(page)
	    corps = get_page_corp_list(url)

    except Exception, e:
	traceback.print_exc()

def get_page_corp_list(url):
    try:
	time.sleep(2)
	html = urllib2.urlopen(url)
        bsObj = BeautifulSoup(html,"lxml")
        items = bsObj.findAll("a",{"class":"logo-box"})
	corps = []
	print 'items_size = ' + str(len(items))
	if items is not None and len(items) > 0:
	    for item in items:
		corp_info = get_corp_info(item["href"])
		if corp_info is not None:
		    corps.append(corp_info)
		time.sleep(2)

	corps = compose_corps_with_follow(corps)
#	print jsonpickle.encode(corps)
	return corps

    except Exception, e:
	traceback.print_exc()

def get_corp_info(url):
    try:
	print "corp_url:\t" + url
	time.sleep(2)
        html = urllib2.urlopen(url)
        bsObj = BeautifulSoup(html,"lxml")
	corp_name = bsObj.find("div",{"class":"name-and-welfare"}).find("h1").text.strip()
	corp_name = corp_name[:len(corp_name) - 5]
	corp_logo = bsObj.find("img",{"class":"bigELogo"})["src"]
#	corp_follow = get_follow_number(url)
	corp_follow = 0
	corp_summary = ''
	if bsObj.find("p",{"class":"profile"}) is not None:
	    corp_summary = bsObj.find("p",{"class":"profile"}).text.strip()[:2000]

	corp_industry_text = bsObj.find("ul",{"class":"new-compintro"}).findAll("li")[0].text
	corp_industry  = corp_industry_text[corp_industry_text.find(u'：')+1:].strip()
	corp_addr = bsObj.find("ul",{"class":"new-compintro"}).findAll("li")[2]["title"]
	
	corp_base_url = url[:len(url) - 1]
	lid = corp_base_url[corp_base_url.rfind("/")+1:]

#	print "corp_name:\t"  + corp_name
#	print "corp_logo:\t"  + corp_logo
#	print "corp_follow:\t"  + str(corp_follow)
#	print "corp_industry:\t"  + corp_industry
#	print "corp_addr:\t"  + corp_addr
#	print "corp_summary:\t"  + corp_summary
	print "*" * 120

	return {"lid":lid, "name":corp_name, "logo":corp_logo, "follow":corp_follow, "industry":corp_industry,"addr":corp_addr, "summary":corp_summary}

    except Exception, e:
	traceback.print_exc()
	return None

def compose_corps_with_follow(corps):
    lids = [corp['lid'] for corp in corps]
    follow_num_map = get_follow_numbers_by_lids(lids)
    for corp in corps:
	corp['follow'] = follow_num_map[corp['lid']]
    return corps

def get_follow_numbers_by_lids(ids):
    try:
	id_str = ''
	for id in ids:
	    id_str = id_str + str(id) + ','

	form_map = {'userh_ids':id_str}
	head_map = {'X-Requested-With' : 'XMLHttpRequest'}
	
	follow_base_url = 'https://c.liepin.com/connection/loadattention-b.json'
	data = urllib.urlencode(form_map)
	req = urllib2.Request(follow_base_url, headers=head_map, data=data)
	json_data = urllib2.urlopen(req).read()
	json_array = jsonpickle.decode(json_data)['data']['attentions']
	follow_map = {}
	for json_obj in json_array:
	    follow_map[json_obj['userh_id']] = json_obj['attention_cnt']
	return follow_map
	
    except Exception, e:
	traceback.print_exc()
    return None

def get_follow_number(corp_base_url):
    follow_base_url = 'https://c.liepin.com/connection/loadattention-b.json'
    corp_base_url = corp_base_url[:len(corp_base_url) - 1]
    corp_id = corp_base_url[corp_base_url.rfind("/")+1:]
    form_map = {'userh_ids':corp_id}
    head_map = {'X-Requested-With' : 'XMLHttpRequest'}
    time.sleep(5)
    data = urllib.urlencode(form_map)
    req = urllib2.Request(follow_base_url, headers=head_map, data=data)
    json_data = urllib2.urlopen(req).read()
    return jsonpickle.decode(json_data)['data']['attentions'][0]['attention_cnt']



category_urls = get_industry_category_urls()
for category_url in category_urls[3:4]:
    print category_url
    get_industry_corp_list(category_url)
#get_corp_info('https://www.liepin.com/company/8405646/')
#get_follow_number('https://www.liepin.com/company/2174886/')
